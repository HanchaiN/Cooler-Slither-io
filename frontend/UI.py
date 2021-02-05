# oh, I know how to use module. I can make them myself
import requests # this work in standatd CPython, but not in JavaPython, so bye
import drawer # this is what client suppose to have, the display
# bot is optimal if that user will use it, no detection was implemented
import json # secure and readable format

name='Player'
url='localhost:8000'
data={}
id=-1

def create(): # spawn our fellow slither
    r=requests.post(f'{url}',data)
    id=int(r.text)
def get(): # ask for game status
    r=requests.get(f'{url}')
    return r.json()
def turn(a): # turn it
    r=requests.post(f'{url}/{id}',{'angle':a})
def delete(): # and remove it
    r=requests.delete(f'{url}/{id}')

def setup():
    size(1000,1000) # screen size
    frameRate(30) # for some smoother(?) animation
    create()
def draw():
    d=get()
    if id not in d['slithers']: # you didn't even exist
        pass # some graphics or function
        return # but I cancled it
    if d['slithers'][id]['embed']['status']=='dead': # you died
        pass # some graphics or function
        delete()
        return # but I cancled it
    drawer.showmap(d,id) # show map with our id as main
    if id in d['slithers'] and d['slithers'][id]['embed']['status']=='live': # instead if the player died we just skip 
        turn(atan2(mouseY-height/2,mouseX-width/2)) # If you can make me some joystick, it will be more helpful