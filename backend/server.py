import backend
import time # to track ticks per sec
import json # to handle input
import threading # to calculate and manage http at once

g=backend.fullmap(1000) # here's come our map

# Here I come. HTTPs setup.
import flask
import flask_restful

app = flask.Flask(__name__)
api = flask_restful.Api(app)

class GlobalHandler(flask_restful.Resource):
    def get(self):
        return g.export(), 200
    def post(self):
        return g.spawn(json.loads(flask.request.form['data'])), 201
class LocalHandler(flask_restful.Resource):
    def put(self,id):
        parser = flask_restful.reqparse.RequestParser()
        parser.add_argument('angle',type=float)
        args = parser.parse_args()
        if g.turn(id,args['angle']):
            return '', 204
        else:
            abort(404,message=f'{id} doesn't exist')
    def delete(self,id):
        s=g.remove(id,args['angle'])
        if s==0:
            abort(404,message=f'{id} doesn't exist')
        elif s==2:
            return '',202
        elif s==4:
            return '',204
        else:
            abort(500)

api.add_resource(GlobalHandler,'/')
api.add_resource(LocalHandler,'/<int:id>')

def handler():
    app.run()

# Standard run
def calculate():
    delta=0
    backend.delta=lambda: delta
    while True:
        t=time.time_ns()
        with locker:
            g.update()
        delta=0.5*delta+0.5*10**(-9)*(time.time_ns()-t)

# initiate the threads
locker=threading.Lock()
handler_=threading.Thread(target=httphandler)
handler_.daemon=True
calculate_=threading.Thread(target=calculate)
calculate_.daemon=True

# run
handler_.start()
calculate_.start()