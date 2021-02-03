import json

def __showpallet(p): # {pos:[x,y],rad:...}
    fill(0) # very bad color for the pallet
    noStroke()
    circle(p['pos'][0],p['pos'][1],2*p['rad'])
def __shownode(n): # again but with other color # {pos:[x,y],rad:...}
    fill(255)
    stroke(0)
    strokeWeight(1)
    circle(n['pos'][0],n['pos'][1],2*n['rad'])
def __showtentacle(tent): # {vol:...,nodes:[...n]}
    for n in tent['nodes']:
        __shownode(n) # run nodes there
def showmap(full,main=''): # some shame graphic # {r:...,slithers:{...tent},pallets:[...p]}
    if main in full['slithers']: # if we focus on exist slither
        print(full['slithers'][main]['vol']) # status export huh
        translate(width/2,height/2)
        scale(100*0.5/full['slithers'][main]['nodes'][0]['rad']) # scale so that the head is of size 100 ( if you may implement me some uh smooth transition, it'll be nice)
        translate(-full['slithers'][main]['nodes'][0]['pos'][0],-full['slithers'][main]['nodes'][0]['pos'][1]) # and make sure that the slither is in the center
    else: # or if you're dead you will look at the entire map aka minimap
        id=''
        v=0
        for i in full['slithers']:
            if full['slithers'][i]['vol']>v:
                v=full['slithers'][i]['vol']
                id=i
        if id in full['slithers']:
            showmap(data,id) # or just follow highscore slither?
            return
        translate(width/2,height/2) # move the map to the center
        scale(min(width,height)*0.5/full['r']) # try to fit all map inside
    stroke(255,0,0)
    strokeWeight(10)
    fill(128)
    circle(0,0,2*full['r']) # don't forget the border line to warn you
    for p in full['pallets']:
        __showpallet(p) # the pallets here
    for t in full['slithers']:
        __showtentacle(full['slithers'][t]) # slithers there
