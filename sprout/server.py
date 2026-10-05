"""Read-only local HTTP API for the sample plant collection."""
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from sprout.reminders import due_plants, load_plants, load_settings


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/api/reminders':
            self.send_error(404)
            return
        settings = load_settings()
        payload = json.dumps(due_plants(load_plants(), date.today(), settings)).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(payload)


if __name__ == '__main__':
    HTTPServer(('127.0.0.1', load_settings()['port']), Handler).serve_forever()
