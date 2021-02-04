import backend
import time # to track ticks per sec
import json # to handle input
import threading # to calculate and manage http at once

g=backend.fullmap(1000) # here's come our map

# Here I come. HTTPs setup.
import http.server
import socketserver

from io import BytesIO

class handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        with locker:
            self.wfile.write(bytes(g.export(), 'utf-8'))

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        with locker:
            if(g.spawn(json.loads(body)['id'])):
                self.send_response(201)
            else:
                self.send_response(208)
            self.end_headers()
        response = BytesIO()
        response.write(body)
        self.wfile.write(response.getvalue())

    def do_PUT(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        with locker:
            if(g.turn(json.loads(body)['id'],json.loads(body)['angle'])):
                self.send_response(202)
            else:
                self.send_response(404)
            self.end_headers()
        response = BytesIO()
        response.write(body)
        self.wfile.write(response.getvalue())
def httphandler():
    httpd = socketserver.TCPServer(('localhost', 8000), handler)
    httpd.serve_forever()

# Standard run
def calculate():
    delta=0
    backend.delta=lambda: delta
    while True:
        t=time.time_ns()
        with locker:
            g.update()
        delta=0.5*delta+0.5*10**(-9)*(time.time_ns()-t)
        print(delta)

# initiate the threads
locker=threading.Lock()
httphandler_=threading.Thread(target=httphandler)
# httphandler_.daemon=True
calculate_=threading.Thread(target=calculate)
# calculate_.daemon=True

# run
httphandler_.start()
calculate_.start()