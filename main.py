import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers_and_answer(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps({'ok': True}), encoding='utf-8'))

    # def log_request(self, code='-', size='-'):
    #     """ Override log requests """

    def do_GET(self):
        query = urllib.parse.parse_qs(self.path[2:], keep_blank_values=True)
        payload = {}
        for key in query.keys():
            payload[key] = query[key][0]

        call_action(payload)
        self._set_headers_and_answer()

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        payload = json.loads(self.rfile.read(length))

        call_action(payload)
        self._set_headers_and_answer()


def call_action(payload):
    print(payload)


def main():
    httpd = HTTPServer(('', 5501), HTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
