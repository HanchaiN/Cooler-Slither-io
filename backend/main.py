# Hanchai Nonprasart

import backend
import clients
import json # to handle input
import threading # to calculate and manage http at once

g=backend.fullmap(1000) # here's come our map
db=clients.authentation()

# Here I come. HTTPs setup.
import flask
import flask_restful
import flask_httpauth

app = flask.Flask(__name__)
api = flask_restful.Api(app)
auth = flask_httpauth.HTTPBasicAuth()

@auth.verify_password
def verify_password(user, pwd): # maybe we can make user just use their account instead
	return db.login(user, pwd) # identity number of this client
@auth.get_user_roles
def get_user_roles(user): # we may have roles, for each player and admin to mess with gamerule, Let's prepare for it
	return db.role(user[0])

# anyone can get data
# login to create the slither and gained player role
# login as player give you permission to control your corresponding slither
# you can signup somewhere else first

class GameplayHandler(flask_restful.Resource):
	def get(self):
		return g.export(), 200
	@auth.login_required(role=['user']) # sadly admin can't play it directly.
	def post(self):
		data=json.loads(flask.request.get_data())
		try:
			assert type(data['public'])==dict
			assert type(data['private'])==dict
			usr=auth.current_user()
			data['private']['username']=usr[0]
			assert db.join(usr[0],usr[1],'player',g.spawn(data))
		except:
			flask_restful.abort(400)
		return '', 201
	@auth.login_required(role=['player'])
	def put(self):
		parser = flask_restful.reqparse.RequestParser()
		parser.add_argument('angle',type=float)
		args = parser.parse_args()
		if g.turn(auth.current_user()[2]['player'],args['angle']):
			return '', 204
		else:
			return '', 202
	@auth.login_required(role=['player'])
	def delete(self):
		if g.remove(auth.current_user()[2]['player']):
			usr=auth.current_user()
			db.leave(usr[0],usr[1],'player') # no more login in this slither
			return '',204
		else:
			return '',202

class UserHandler(flask_restful.Resource): # accounts management
	def post(self):
		usr=json.loads(flask.request.get_data())
		if db.signup(usr['name'],usr['pwd']):
			return 'succussful', 201
		else:
			return 'username existed', 200
	@auth.login_required
	def put(self):
		new=json.loads(flask.request.get_data())
		old=auth.current_user()
		db.update(usr['name'],usr['pwd'],old[0],old[1])
		return 'succussful', 201
	@auth.login_required(role=['admin'])
	def get(self):
		usr=auth.current_user()
		return db.view(usr[0],usr[1]),200

class AdminHandler(flask_restful.Resource): # may be implement long later
	@auth.login_required(role=['admin'])
	def get(self):
		usr=auth.current_user()
		return db.view(usr[0],usr[1]),200

@app.route('/')
def main():
	return 'Go to /user to manage account and /play to play'

api.add_resource(GameplayHandler,'/play') # gameplay api
api.add_resource(UserHandler,'/user') # account api
api.add_resource(AdminHandler,'/user/admin') # admin account api

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
		with locker:
			fps,event=g.update()
		if 'win' in event:
			for i in event['win']:
				db.setdata(i,{'slither':'winned'})


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