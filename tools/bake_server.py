"""나무 이미지 카드 제작용 로컬 서버.

python tools/bake_server.py <모델 폴더> <출력 폴더>
tools/, /models/ 를 제공하고 POST /save?name=... 로 받은 RGBA 픽셀을 저장한다.
"""
import http.server
import os
import sys
import urllib.parse

MODELS, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = urllib.parse.unquote(path.split('?')[0])
        if path.startswith('/models/'):
            return os.path.join(MODELS, path[len('/models/'):])
        return os.path.join(HERE, path.lstrip('/'))

    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        data = self.rfile.read(int(self.headers['Content-Length']))
        with open(os.path.join(OUT, os.path.basename(q['name'][0])), 'wb') as f:
            f.write(data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

    def log_message(self, *args):
        pass


http.server.ThreadingHTTPServer(('127.0.0.1', 8771), Handler).serve_forever()
