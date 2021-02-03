import backend
import time # to track ticks per sec
import json # to handle input

# initial setup
g=backend.fullmap(1000)

# Here I come. HTTPs setup.
import http.server
import socketserver

from io import BytesIO

class handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(g.export(), 'utf-8'))

    def do_HEAD(self):
        pass

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        print(body)
        print(g.spawn(json.loads(body)['id']))
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        self.wfile.write(response.getvalue())

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        self.wfile.write(response.getvalue())

httpd = socket.TCPServer(('localhost', 8000), handler)
httpd.serve_forever()

# Standard run
delta=0
backend.delta=lambda: delta
while True:
    t=time.time_ns()
    g.update()
    delta=0.5*delta+0.5*10**(-9)*(time.time_ns()-t)