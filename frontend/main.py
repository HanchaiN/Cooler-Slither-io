# Hanchai Nonprasart

# oh, I know how to use module. I can make them myself
import requests # this work in standatd CPython, but not in JavaPython, so bye
# bot is optimal if that user will use it, no detection was implemented
import json # secure and readable format

url='https://csi-backend.mwit308.repl.co' # we host our server on repl.it

pwd='qwerty'
name='User'
data={'public':{'name':'Player'},'private':{}}

def signup(): # 201: new user created, 200: user existed but not tested if it is correct password or not
	global iden, data, url
	r=requests.post(f'{url}/user',json={'name':name,'pwd':pwd})
	print(r.status_code)
def create(): # spawn our fellow slither
	global name, url, pwd, data
	r=requests.post(f'{url}/play',json=data, auth=requests.auth.HTTPBasicAuth(name,pwd))
	print(r.status_code)
def get(): # ask for game status
	global url
	r=requests.get(f'{url}/play')
	print(r.status_code)
	return r.json()
def status():
	global name, url, pwd
	r=requests.get(f'{url}/play', auth=requests.auth.HTTPBasicAuth(name,pwd))
	print(r.status_code)
	return r.json()
def turn(a): # turn it
	global name, url, pwd
	r=requests.put(f'{url}/play', json={'angle':a}, auth=requests.auth.HTTPBasicAuth(name,pwd))
	print(r.status_code)
def delete(): # and remove it
	global iden, url, pwd
	r=requests.delete(f'{url}/play', auth=requests.auth.HTTPBasicAuth(iden,pwd))
	print(r.status_code)

signup() # api test
create()
# delete()

import snake # graphic test
s=snake.SNAKE()