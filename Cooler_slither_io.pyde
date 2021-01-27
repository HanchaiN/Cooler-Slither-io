# oh, I know how to use module. I can make them myself
import server # assume that it is possible for you to do it yourself
import client # this is what client suppose to have, the display
# bot is optimal if that user will use it, no detection was implemented

g=server.fullmap(1000) # let make our server or in case that you are the client, the server connection
name='Player'
def setup():
    global g # idk if this is necessary but game is global variable
    size(1000,1000) # screen size
    g.slither(name) # you were spawn but it suppose to run through suppose to using http POST
    frameRate(30) # for some smoother(?) animation
def draw():
    print(frameRate) # some little status
    global g # idk if this is necessary but game is global variable
    g.update() # then we update the map on each server tick (which suppose to be really low)
    d=g.export() # this was suppose to be on server respond upon using http GET method, so I will just use the file instead
    if name not in g.slithers: # you died or doesn't spawn yet
        pass # some graphics or function
        # return # but I cancled it
    background(255,128,128) # just bad died graphic
    client.showmap(d,name) # Let try to focus on our slither based on data in the server from http GET method
    if name in g.slithers: # instead if the player died we just skip 
        angle=PVector(mouseX-width/2,mouseY-height/2).heading() # If you can make me some joystick, it will be more helpful
        g.turn(name,angle) # updating the slither to the server which suppose to using http PUT, I guess
        # if you just left (in the real server), it will be like you afk, not disappear or dead so be aware.
