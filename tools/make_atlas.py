"""찍어 낸 나무를 잘라 한 장의 투명 이미지로 합친다.

python tools/make_atlas.py <출력 폴더> <모델> <촬영 크기> <칸 높이> <저장 경로>
결과: <저장 경로>.webp, <저장 경로>.json (칸별 UV, 실제 너비, 높이)
"""
import json
import os
import sys

import numpy as np
from PIL import Image

baked, model, size, cell_h, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
log = json.load(open(os.path.join(baked, model + '.json')))
cells = []
for item in log:
    groups = sorted({x['group'] for x in log})
    g = groups.index(item['group'])
    raw = open(os.path.join(baked, f"{model}_{g}_{item['view']}_{size}.raw"), 'rb').read()
    a = np.frombuffer(raw, dtype='uint8').reshape(size, size, 4)[::-1].astype('float32')
    mask = a[..., 3] > 8
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    crop = a[y0:y1, x0:x1]
    # 어두운 가장자리가 생기지 않도록 알파를 곱한 상태로 줄인다.
    crop[..., :3] *= crop[..., 3:] / 255
    meters = 2 * item['half'] / size
    w_m, h_m = (x1 - x0) * meters, (y1 - y0) * meters
    # 나무 줄기가 칸 중심에 오도록 원래 중심까지의 거리를 기록한다.
    cx = (size / 2 - x0) / (x1 - x0)
    cells.append({'crop': crop, 'w': w_m, 'h': h_m, 'cx': float(cx)})
scale = cell_h / max(c['h'] for c in cells)
layout, x = [], 0
imgs = []
for c in cells:
    h = max(4, round(c['h'] * scale))
    w = max(4, round(c['w'] * scale))
    chans = [Image.fromarray(c['crop'][..., i]).resize((w, h), Image.LANCZOS) for i in range(4)]
    imgs.append((chans, x, w, h))
    layout.append({'x': x, 'w': w, 'h': h, 'width': c['w'], 'height': c['h'], 'cx': c['cx']})
    x += w + 4
W, H = x, cell_h
atlas = np.zeros((H, W, 4), 'float32')
for chans, px, w, h in imgs:
    arr = np.dstack([np.asarray(ch) for ch in chans])
    atlas[H - h:H, px:px + w] = arr
al = np.clip(atlas[..., 3:], 0, 255)
rgb = np.where(al > 1, atlas[..., :3] * 255 / np.maximum(al, 1), 0)
# 달빛의 푸른 기운을 줄여 눈이 창백하게 보이게 한다.
luma = rgb.mean(2, keepdims=True)
rgb = luma * np.array([.92, .96, 1.04]) * .72 + rgb * .28
# 투명한 곳에 평균색을 채워 밉맵에서 검게 번지지 않게 한다.
opaque = al[..., 0] > 40
fill = rgb[opaque].mean(0)
rgb[al[..., 0] <= 1] = fill
result = np.dstack([np.clip(rgb, 0, 255), al]).astype('uint8')
Image.fromarray(result, 'RGBA').save(out + '.webp', 'WEBP', quality=82, alpha_quality=85, method=4)
for l in layout:
    l['u0'], l['u1'], l['v1'] = l['x'] / W, (l['x'] + l['w']) / W, l['h'] / H
json.dump({'w': W, 'h': H, 'cells': layout}, open(out + '.json', 'w'))
print(model, W, H, os.path.getsize(out + '.webp') // 1024, 'KB', [(round(l['width'], 1), round(l['height'], 1)) for l in layout])
bg = np.full((H, W, 3), [10, 14, 28], 'float32')
prev = result[..., :3] * (al / 255) + bg * (1 - al / 255)
Image.fromarray(prev.astype('uint8')).resize((W * 900 // H, 900) if W * 900 // H < 2000 else (2000, H * 2000 // W), Image.LANCZOS).save(out + '_prev.jpg', quality=88)
