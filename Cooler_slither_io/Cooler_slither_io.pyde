# oh, I know how to use module. I can make them myself
import http.client # this work in standatd CPython, but not in JavaPython, so bye
import client # this is what client suppose to have, the display
# bot is optimal if that user will use it, no detection was implemented
import json # secure and readable format

name='Player'
url='localhost:8000'
server=http.client.HTTPConnection(url)
def setup():
    size(1000,1000) # screen size
    frameRate(30) # for some smoother(?) animation
    server.request("POST","/",body=json.dumps({'id':name})) # spawn our fellow slither
    server.getresponse().read() # clear cache
def draw():
    server.request("GET","/") # ask for game status
    d=json.loads(server.getresponse().read()) # parse to dictionary-list type
    if name not in d['slithers']: # you died or doesn't spawn yet
        pass # some graphics or function
        # return # but I cancled it
    background(255,128,128) # just bad died graphic
    client.showmap(d,name) # Let try to focus on our slither based on data in the server from http GET method
    if name in d['slithers']: # instead if the player died we just skip 
        angle=atan2(mouseY-height/2,mouseX-width/2) # If you can make me some joystick, it will be more helpful
        server.request("PUT","/",body=json.dumps({'id':name,'angle':angle})) # updating the slither to the server
        # if you just left (in the real server), it will be like you afk, not disappear or dead so be aware.
