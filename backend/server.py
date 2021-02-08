import backend
import time # to track ticks per sec
import json # to handle input
import threading # to calculate and manage http at once

g=backend.fullmap(1000) # here's come our map

# Here I come. HTTPs setup.
import flask
import flask_restful
import flask_httpauth

app = flask.Flask(__name__)
api = flask_restful.Api(app)
auth = flask_httpauth.HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
	if g.login(int(username),str(password)): 
		return int(username)
@auth.get_user_roles
def get_user_roles(user): # we may have roles, for each player and admin to mess with gamerule, Let's prepare for it
	return ['player']


class Handler(flask_restful.Resource):
	def get(self):
		return g.export(), 200
	def post(self):
		data=json.loads(flask.request.get_data())
		try:
			public=data['public']
			private=data['private']
			assert 'pass' in private
		except:
			flask_restful.abort(400)
		return {'id':g.spawn({'public':public,'private':private})}, 201
	@auth.login_required(role=['player'])
	def put(self):
		parser = flask_restful.reqparse.RequestParser()
		parser.add_argument('angle',type=float)
		args = parser.parse_args()
		if g.turn(auth.current_user(),args['angle']):
			return '', 204
		else:
			return '', 202
	@auth.login_required(role=['player'])
	def delete(self):
		if g.remove(auth.current_user()):
			return '',204
		else:
			return '',202

api.add_resource(Handler,'/')

def handler():
	app.run(
			host='0.0.0.0', # in repl.it, it is currently at https://csi-backend.mwit308.repl.co/
			port=8000
		)

# Standard run
def calculate():
	delta=0
	backend.delta=lambda: delta
	while True:
		t=time.time_ns()
		with locker:
			g.update()
		delta=0.5*delta+0.5*10**(-9)*(time.time_ns()-t)
		# print(1/delta) # fps of the server, pretty low huh

# initiate the threads
locker=threading.Lock()
handler_=threading.Thread(target=handler)
handler_.daemon=True
calculate_=threading.Thread(target=calculate)
calculate_.daemon=True

# run
handler_.start()
calculate_.start()
while True:
	pass # wait for force quit