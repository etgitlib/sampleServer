from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
import os

port = int(os.environ.get('PORT', 80))
gloVars = globals()
locVars = locals()

def getQueryParams(query, needKey, default=None):
    query_params = parse_qsl(query)
    for key, value in query_params:
        if needKey == key:
            return value
    return default

def initialize(query):
    global gloVars, locVars
    code = getQueryParams(query, 'code', default = '')
    exec(code, gloVars, locVars)
    return b"200"

_routes = {
    "init": initialize
}

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        parsed = urlparse(self.path)
        handler = _routes.get(parsed.path[1:])
        if handler:
            self.wfile.write(handler(parsed.query))
        else:
            self.wfile.write(b'404')

    def log_message(self, format, *args):
        return

server = HTTPServer(('', port), MyHandler)
print('Starting server, use <Ctrl-C> to stop')
server.serve_forever()