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
	# print(r.status_code)
def create(): # spawn our fellow slither
	global name, url, pwd, data
	r=requests.post(f'{url}/slitherio/play',json=data, auth=requests.auth.HTTPBasicAuth(name,pwd))
	# print(r.status_code)
def get(): # ask for game status as viewer
	global url
	r=requests.get(f'{url}/slitherio/view')
	# print(r.status_code)
	try:
		assert r.status_code==200
		return r.json()
	except:
		return {'r':0,'pallets':{},'slithers':{}}
		# print(r.status_code,r.text)
def getstatus(): # ask for game status as specific user (identity number(may help in drawing), private data, viewer map info)
	global name, url, pwd
	r=requests.get(f'{url}/slitherio/play', auth=requests.auth.HTTPBasicAuth(name,pwd))
	# print(r.status_code)
	try:
		assert r.status_code==200
		return r.json()
	except:
		return {'iden':-1,'user':name,'map':get()}
		# print(r.status_code,r.text)
def turn(a): # turn it
	global name, url, pwd
	r=requests.put(f'{url}/slitherio/play', json={'angle':a}, auth=requests.auth.HTTPBasicAuth(name,pwd))
	# print(r.status_code)
def delete(): # and remove it
	global name, url, pwd
	r=requests.delete(f'{url}/slitherio/play', auth=requests.auth.HTTPBasicAuth(name,pwd))
	# print(r.status_code)
class play(): # dummy class to finish the slither once after another (avoid some bug) # please use keyboard interrupt (ctrl+c) to exit
	def __init__(self):
		pass
	def __enter__(self):
		create()
		return None
	def __exit__(self, type, value, traceback):
		delete()
		pass
import snake
import random,math,time
scr,clk=snake.init()
# if True:
# 	signup()
# 	while True: # spammer client
# 		with play():
# 			a=getstatus()
# 			while True:
# 				try:
# 					assert a['map']['slithers'][str(a['iden'])]['embed']['status']=='live'
# 				except:
# 					break
# 				surf=snake.draw(a['map']) # please don't make too many request.
# 				w,h=scr.get_size()
# 				w=min(w,h)
# 				surf=snake.pygame.transform.scale(surf,(w,w))
# 				mapscreen=snake.pygame.Rect(0,0,w,w)
# 				scr.blit(surf,mapscreen)
# 				snake.pygame.display.update()
# 				turn(random.random()*2*math.pi) # random walker
# 				a=getstatus()
# 				clk.tick(30) # if you could calculate by yourself for a while, I'm so glad.
# 		clk.tick(30)
t=0
while True:
	t=time.time()
	w,h=scr.get_size()
	w=min(w,h)
	d=get()
	surf=snake.draw(d,scale=0.5*w/d['r']) # please don't make too many request.
	# surf=snake.pygame.transform.scale(surf,(w,w))
	mapscreen=snake.pygame.Rect(0,0,w,w)
	scr.blit(surf,mapscreen)
	snake.pygame.display.update()
	dt=time.time()-t
	print(1/dt)
	# clk.tick(30) # real fps, please don't request same frame more than once, it make server even slower