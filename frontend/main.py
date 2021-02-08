# oh, I know how to use module. I can make them myself
import requests # this work in standatd CPython, but not in JavaPython, so bye
# bot is optimal if that user will use it, no detection was implemented
import json # secure and readable format

# test file

url='https://csi-backend.mwit308.repl.co/' # we host our server on repl.it

iden=-1
pwd='qwerty'
data={'public':{'name':'Player'},'private':{'pass':pwd}}

def create(): # spawn our fellow slither
	global iden, data, url
	r=requests.post(f'{url}',json=data)
	iden=r.json()['id']
	print(r.status_code)
def get(): # ask for game status
	global url
	r=requests.get(f'{url}')
	print(r.status_code)
	return r.json()
def turn(a): # turn it
	global iden, url, pwd
	r=requests.put(f'{url}', json={'angle':a}, auth=requests.auth.HTTPBasicAuth(iden,pwd))
	print(r.status_code)
def delete(): # and remove it
	global iden, url, pwd
	r=requests.delete(f'{url}', auth=requests.auth.HTTPBasicAuth(iden,pwd))
	print(r.status_code)
create()
delete()