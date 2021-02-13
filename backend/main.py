# Hanchai Nonprasart

import backend
import clients
import json # to handle input
import threading # to calculate and manage http at once
import os

g=backend.fullmap(1000) # here's come our map
db=clients.authentation()

# Here I come. HTTPs setup.
import flask
import flask_restful
from flask_restful import reqparse
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

class PlayerGameplayHandler(flask_restful.Resource):
	@auth.login_required(role=['slither'])
	def get(self):
		with locker:
			return g.data(auth.current_user()[2]['slither']), 200
	@auth.login_required(role=['user']) # sadly admin can't play it directly.
	def post(self):
		data=json.loads(flask.request.get_data())
		try:
			assert type(data['public'])==dict
			assert type(data['private'])==dict
			usr=auth.current_user()
			data['private']['username']=usr[0]
			p=None
			with locker:
				p=g.spawn(data)
			assert db.join(usr[0],usr[1],'slither',p)
		except:
			flask_restful.abort(400)
		return '', 201
	@auth.login_required(role=['slither'])
	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument('angle',type=float)
		args = parser.parse_args()
		p=None
		with locker:
			p=g.turn(auth.current_user()[2]['slither'],args['angle'])
		if p:
			return '', 204
		else:
			return '', 202
	@auth.login_required(role=['slither'])
	def delete(self):
		p=None
		with locker:
			p=g.remove(auth.current_user()[2]['slither'])
		if p:
			usr=auth.current_user()
			db.leave(usr[0],usr[0],usr[1],'slither') # no more login in this slither
			return '',204
		else:
			return '',202

class ViewerGameplayHandler(flask_restful.Resource):
	def get(self):
		with locker:
			return g.export(), 200

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
	return 'Go to /user to manage account and .../play to play games'
@app.route('/slitherio')
def slitherio():
	return f"{fps}"

api.add_resource(PlayerGameplayHandler,'/slitherio/play') # gameplay api
api.add_resource(ViewerGameplayHandler,'/slitherio/view') # gameplay api
api.add_resource(UserHandler,'/user') # account api
api.add_resource(AdminHandler,'/admin') # admin account api

def handler():
	app.run(
			host='0.0.0.0', # in repl.it, it is currently at https://csi-backend.mwit308.repl.co/
			port=8000
		)

fps=0
# Standard run
import time
def calculate():
	while True:
		global fps
		with locker:
			fps,event=g.update()
		if 'win' in event:
			for i in event['win']:
				db.setdata(i,{'slither':'winned'})
		time.sleep(max(1/30-1/fps,0))
		# if 'del' in event: # manage yourself, this cause a lot of trouble
		# 	for i in event['del']:
		# 		db.leave(i,os.getenv("ADMIN_USR"),os.getenv("ADMIN_PWD"),'slither')


# initiate the threads
class locker(): # dummy locker, increase performance but decrease accuracy (buggy)
	def __init__(self):
		pass
	def __enter__(self):
		return None
	def __exit__(self, type, value, traceback):
		pass
locker= threading.Lock() # decrease perfomance but avoid collision of data
handler_=threading.Thread(target=handler)
handler_.daemon=True
calculate_=threading.Thread(target=calculate)
calculate_.daemon=True

# run
handler_.start()
calculate_.start()
while True:
	pass # wait for force quit