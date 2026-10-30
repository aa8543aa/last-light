"""게임 배경 이미지를 지형 계산으로 렌더링한다. (numpy, Pillow 필요)

python tools/render_mountains.py <출력 폴더>
  night_valley.jpg : 지상 장면의 하늘, 봉우리, 계곡, 마을 불빛
  window_range.jpg : 기내 창밖으로 내려다보는 설산
"""
import sys
import numpy as np
from PIL import Image

N = 4096
CELL = 10.0  # m
W, H = 2048, 1024
rng = np.random.default_rng(1225)
fx = np.fft.fftfreq(N)[:, None]
fy = np.fft.fftfreq(N)[None, :]
fr = np.sqrt(fx * fx + fy * fy)


def band(low, high):
    """low~high 주파수만 남긴 노이즈 (0~1 근처)"""
    spec = np.fft.fft2(rng.normal(size=(N, N)))
    spec *= ((fr >= low) & (fr < high))
    n = np.real(np.fft.ifft2(spec))
    return np.clip(n / (n.std() * 4) + .5, 0, 1)


def ridged(start=1 / 700, octaves=7, gain=.52):
    h, amp, w, f = np.zeros((N, N)), .5, np.ones((N, N)), start
    for _ in range(octaves):
        r = 1 - np.abs(2 * band(f, f * 1.9) - 1)
        s = r * r * w
        h += s * amp
        w = np.clip(s * 2.2, 0, 1)
        amp *= gain
        f *= 2
    return h


def shade(h, moon_elev):
    gx, gy = np.gradient(h, CELL)
    nz = 1 / np.sqrt(gx * gx + gy * gy + 1)
    nx, ny = -gx * nz, -gy * nz
    sun = np.array([.72, .34, .6])
    sun /= np.linalg.norm(sun)
    lam = np.clip(nx * sun[0] + ny * sun[1] + nz * sun[2], 0, 1)
    # 달빛이 x축 방향에서 오는 그림자
    t = np.tan(moon_elev)
    key = h + np.arange(N)[:, None] * CELL * t
    lit = key >= np.maximum.accumulate(key, axis=0) - 2
    return lam * (lit * .86 + .14), nz


def albedo(h, nz, snow_low, snow_high):
    d = band(1 / 40, 1 / 6)
    alt = np.clip((h - snow_low) / (snow_high - snow_low) + (d - .5) * .7, 0, 1)
    flat = np.clip((nz - .3) / .16 + (band(1 / 14, 1 / 3) - .5) * 1.1, 0, 1)
    snow = alt * flat
    rock = .035 + band(1 / 70, 1 / 4) * .1
    return rock * (1 - snow) + .94 * snow


def render(h, col, cam, pitch_v, focal, fog_len, fog_col, sky, yaw=0.):
    """높이맵을 앞에서 뒤로 훑어 그리는 열 단위 렌더러"""
    ds = np.geomspace(60, 36000, 2600)
    out = sky.copy()
    horizon = pitch_v * H
    for px in range(W):
        a = yaw + np.arctan((px - W / 2) / focal)
        ca, sa = np.cos(a), np.sin(a)
        dist = ds / np.maximum(ca, .2)
        fxs = np.clip((cam[0] + ds * sa / np.maximum(ca, .2)) / CELL, 0, N - 1.001)
        fzs = np.clip((cam[1] + ds) / CELL, 0, N - 1.001)
        ix, iz = fxs.astype(int), fzs.astype(int)
        tx, tz = fxs - ix, fzs - iz
        def lerp2(a):
            wx, wz = (tx, tz) if a.ndim == 2 else (tx[..., None], tz[..., None])
            return (a[ix, iz] * (1 - wx) + a[ix + 1, iz] * wx) * (1 - wz) + (a[ix, iz + 1] * (1 - wx) + a[ix + 1, iz + 1] * wx) * wz
        y = horizon + (cam[2] - lerp2(h)) / dist * focal
        samples = lerp2(col)
        acc = np.minimum.accumulate(y)
        rows = np.arange(H)
        idx = np.searchsorted(-acc, -rows.astype(float))
        hit = idx < len(ds)
        c = samples[idx[hit]]
        fog = (1 - np.exp(-dist[idx[hit]] / fog_len))[..., None]
        out[hit, px] = c * (1 - fog) + fog_col * fog
    return out


def starry_sky(zenith, horizon_col, horizon_v):
    v = np.linspace(0, 1, H)[:, None]
    t = np.clip(v / horizon_v, 0, 1)[..., None] ** 1.5
    sky = np.array(zenith) * (1 - t) + np.array(horizon_col) * t
    sky = np.repeat(sky, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    # 은하수처럼 비스듬한 빛 띠
    def smooth_noise(cells_x, cells_y):
        g = rng.random((cells_y, cells_x))
        im = Image.fromarray((g * 255).astype('uint8')).resize((W, H), Image.BICUBIC)
        return np.asarray(im) / 255.
    n = smooth_noise(14, 7) * .55 + smooth_noise(40, 20) * .3 + smooth_noise(120, 60) * .15
    bandline = np.exp(-(((y / H - .24) - (x / W - .5) * .28) / .17) ** 2)
    glow = np.clip(n - .32, 0, 1) * bandline * 1.15
    sky += glow[..., None] * np.array([.17, .23, .33])
    for _ in range(9000):
        sx, sy = rng.integers(0, W), int(rng.random() ** 1.2 * H * horizon_v)
        b = rng.random() ** 5 * .95 + .07
        tint = np.array([1, .96, .9]) if rng.random() < .25 else np.array([.84, .91, 1])
        sky[sy, sx] = np.maximum(sky[sy, sx], tint * b)
        if b > .55:
            for dx, dy, f in [(1, 0, .45), (-1, 0, .45), (0, 1, .45), (0, -1, .45), (2, 0, .13), (-2, 0, .13), (0, 2, .13), (0, -2, .13)]:
                yy, xx = np.clip(sy + dy, 0, H - 1), np.clip(sx + dx, 0, W - 1)
                sky[yy, xx] = np.maximum(sky[yy, xx], tint * b * f)
    return sky


def lenticular(sky, cx, cy, width, height):
    y, x = np.mgrid[0:H, 0:W]
    d = ((x - cx) / width) ** 2 + ((y - cy) / height) ** 2
    a = np.clip(1 - d, 0, 1) ** 1.4 * .62
    a *= .75 + .25 * np.sin(y * .32 + x * .012)
    return sky * (1 - a[..., None]) + np.array([.47, .49, .56]) * a[..., None]


def finish(img):
    img = np.clip(img, 0, None)
    img = img * 1.25 / (1 + img * .28)
    noise = rng.normal(0, .006, img.shape[:2])[..., None]
    return np.clip(np.power(np.clip(img + noise, 0, 1), 1 / 1.9) * 255, 0, 255).astype('uint8')


def valley():
    base = ridged(start=1 / 900, octaves=7, gain=.46)
    xs, zs = np.meshgrid(np.arange(N) * CELL, np.arange(N) * CELL, indexing='ij')
    cx, cam_z = N * CELL * .5, 2000.
    pkx, pkz = cx + 1700, cam_z + 15000.
    # 네 면을 가진 뾰족한 주봉과 그 아래로 뻗은 능선
    dx, dz = xs - pkx, zs - pkz
    pyramid = np.abs(dx * .74 + dz * .67) + np.abs(dx * .67 - dz * .74)
    peak = np.clip(1 - pyramid / 8600, 0, 1) ** 1.25 * 4700
    massif = np.exp(-(((dx + 2300) / 8200) ** 2 + (dz / 3400) ** 2)) * 1750
    # 카메라 양옆으로 가파르게 솟은 어두운 계곡 벽
    lateral = np.abs(xs - cx - np.sin(zs / 2600) * 450) / 1000
    near = np.clip(1 - (zs - cam_z) / 11000, 0, 1)
    walls = np.clip(lateral - .55, 0, None) ** 1.25 * 760 * (.3 + near * 1.2)
    h = base * 900 + walls + peak + massif
    ridge_cut = base ** 1.5 * (peak / 4700) * 520
    h = h + ridge_cut
    light, nz = shade(h, np.radians(24))
    alb = albedo(h, nz, 1750, 2350)
    tree_dark = np.clip((1700 - h) / 900, 0, 1)
    alb = alb * (1 - tree_dark * .55)
    col = (light * alb * 2.5 + .0075)[..., None] * np.array([.76, .86, 1.])
    sky = starry_sky([.006, .015, .04], [.075, .16, .27], .66)
    sky = lenticular(sky, W * .47, H * .36, 140, 17)
    img = render(h, col, (cx, cam_z, 900.), .63, 770, 25000, np.array([.038, .08, .145]), sky)
    # 계곡 바닥의 마을 불빛
    vx, vy = W * .515, H * .655
    for _ in range(260):
        px = int(rng.normal(vx, 22)); py = int(rng.normal(vy, 7) + (px - vx) * .04)
        b = rng.random() ** 2 * 1.4 + .25
        c = np.array([1, .62, .23]) * b
        img[py:py + 2, px:px + 2] = np.maximum(img[py:py + 2, px:px + 2], c)
    y, x = np.mgrid[0:H, 0:W]
    halo = np.exp(-(((x - vx) / 62) ** 2 + ((y - vy) / 24) ** 2))
    img += halo[..., None] * np.array([.1, .05, .014])
    return finish(img)


def window_view():
    base = ridged(start=1 / 2600, octaves=8, gain=.47)
    h = base * 4300
    light, nz = shade(h, np.radians(20))
    alb = albedo(h, nz, 250, 800)
    col = (light * alb * 2.2 + .008)[..., None] * np.array([.74, .85, 1.])
    sky = starry_sky([.004, .012, .035], [.07, .15, .27], .2)
    img = render(h, col, (N * CELL * .5, 900., 5600.), .22, 760, 21000, np.array([.05, .1, .18]), sky, yaw=.02)
    return finish(img)


if __name__ == '__main__':
    out = sys.argv[1]
    Image.fromarray(valley()).save(f'{out}/night_valley.jpg', quality=88, optimize=True)
    Image.fromarray(window_view()).save(f'{out}/window_range.jpg', quality=86, optimize=True)
