# I'm too lazy to use __ to make local here, so be it. Suit yourself, hack all you want.

import basic
import json # secure and readable format
import pickle # just dumb it

class fullmap: # the full server have come
    def __init__(self,radius):
        self.r=radius
        self.slithers={} # list of slither, using some IDs
        self.pallets=[] # and simply list of pallets
    def slither(self,id): # spawn new slither of ID at pos
        pos=PVector.mult(PVector.random2D(),self.r*random(0.2,0.8)) # wish you have lucky spawn
        if id in self.slithers: # sorry but this ID existed
            return False
        self.slithers[id]=basic.tentacle(pos,25,5) # and its time to create the new one with optimized variable (size,length)
    def __objectlist(self): # we need to list objects for collision detection
        objects=[]
        for i in range(len(self.pallets)):
            objects.append({'pos':self.pallets[i].pos,'rad':self.pallets[i].rad,'data':{'type':'pallet','index':i}})
        for i in self.slithers:
            j=0
            for n in self.slithers[i]:
                objects.append({'pos':n.pos,'rad':n.rad,'data':{'type':'slither','index':i,'location':j}})
                j+=1
        return objects # well I just include all object in the game one-by-one
    def update(self): # again updating time aka update()
        col=self.collision(self.bvh(self.__objectlist())) # these function will be explianed later
        dead=set([]) # we need to track for the dead one
        eaten=set([]) # and also the eaten pallet
        for i in col: # check each (detected) collision
            i.sort(key=lambda x:x['data']['type']) # for my hand's health (which was gone long ago) we will eliminate some useless choices by arrange the type of objects
            if i[0]['data']['type']=='pallet':
                if i[1]['data']['type']=='pallet':
                    if self.pallets[i[1]['data']['index']].rad<25 and not(i[0]['data']['index'] in eaten or i[1]['data']['index'] in eaten): # pallet and pallet will merge but to avoid oversize (25++ I guess) and lost of volume : we have this condition
                        eaten.add(i[0]['data']['index']) # mark as eaten
                        self.pallets[i[1]['data']['index']].pos=self.pallets[i[1]['data']['index']].pos.lerp(self.pallets[i[0]['data']['index']].pos,self.pallets[i[1]['data']['index']].rad**2/(self.pallets[i[0]['data']['index']].rad**2+self.pallets[i[1]['data']['index']].rad**2)) # longest line huh, this lead new pallet to be at position between the old one weighted by their volume
                        self.pallets[i[1]['data']['index']].consume(self.pallets[i[0]['data']['index']].rad*self.pallets[i[0]['data']['index']].rad) # time to consume (and as I said we ignored PI
                elif i[1]['data']['type']=='slither':
                    if i[1]['data']['location']==0 and not i[0]['data']['index'] in eaten: # to avoid double eating and to make sure that it was eated from the head
                        eaten.add(i[0]['data']['index']) # bla bla bla same as previous one
                        self.slithers[i[1]['data']['index']].consume(self.pallets[i[0]['data']['index']].rad*self.pallets[i[0]['data']['index']].rad)
                else:
                    pass # this not suppose to exist for now
            elif i[0]['data']['type']=='slither':
                if i[1]['data']['type']=='slither':
                    i.sort(key=lambda x:x['data']['location']) # again
                    if i[0]['data']['index']!=i[1]['data']['index'] and i[0]['data']['location']==0: # to not eat itself and to make sure that it was hitted at the head
                        dead.add(i[0]['data']['index']) # now he's dead
                else:
                    pass # again
            else:
                pass # again
        for i in range(len(self.pallets)): # idk how but the pallet drop out side the map
            if self.pallets[i].pos.mag()>self.r-self.pallets[i].rad:
                eaten.add(i) # boom the border eated you 555
        eaten=list(eaten) # list eaten pallet
        eaten.sort(reverse=True) # and sort it so when we pop it out, it doesn't effect the index of others
        for i in eaten:
            self.pallets.pop(i) # pop the pallet gone
        for i in self.slithers: # check if it dead by the border
            if self.slithers[i].node.pos.mag()>self.r-self.slithers[i].node.rad:
                dead.add(i) # boom
        dead=list(dead)
        for i in dead: # again but we have to care about drop
            for n in self.slithers[i]:
                k=randomGaussian()+n.rad*n.rad # drop random amount for the volume about the dead node
                k/=10*10 # and divided by the size of new pallet (10 I guess)
                if k<0:
                    k=0 # make sure that no error from k<0
                k=floor(k) # and from k not integer
                for j in range(k):
                    loc=PVector(randomGaussian(),randomGaussian())
                    loc=PVector.mult(loc,n.rad/3)
                    loc=PVector.add(loc,n.pos)
                    self.pallets.append(basic.pallet(loc,10)) # place standard (10) pallet at somewhere that 0.2% (+-3sigma) out of the axist
            del self.slithers[i] # and it was completely removed
        for t in self.slithers:
            self.slithers[t].update() # update the slithers, now!
        if len(self.pallets)<0.2*(self.r/10)**2: # we didn't want to be in flood of pallets, right so let say 0.2 of the area
            self.pallets.append(basic.pallet(PVector.mult(PVector.random2D(),random(self.r)),10)) # this make the center have more pallet density than that of the border but different ways from when it drop from the dead (10 is that same constant btw (I may want to random it from 10(smallest) to 25(biggest limit)))
    def turn(self,id,angle): # anyone with id can turn the slither to that angle
        if id in self.slithers:
            self.slithers[id].angle=angle
    def export(self): # all data of all user is here tho, so hacks is o=possible if you don't apply some filter
        d={'r':self.r,'slithers':{},'pallets':[]}
        for p in self.pallets:
            d['pallets'].append({'pos':[p.pos.x,p.pos.y],'rad':p.rad})
        for t in self.slithers:
            d['slithers'][t]={'vol':self.slithers[t].vol,'nodes':[]}
            for n in self.slithers[t]:
                d['slithers'][t]['nodes'].append({'pos':[n.pos.x,n.pos.y],'rad':n.rad})
        return json.dumps(d)
    def store(self): # take this
        pickle.dumb(self,open('save.bin','wb')) # I'm too lazy to modify this to json and then import back, so I just dump it all
    @staticmethod
    def load(): # and pick this
        return pickle.load(open('save.bin','rb'))
    @staticmethod
    def bvh(obj,axis='x'): # bounding volume hierarchy is the nice idea for our case, GO DO RESEARCH YOURSELF
        if len(obj)==0:
            return []
        if len(obj)==1: # end node now
            return obj[0]
        if axis=='x':
            obj.sort(key=lambda a: a['pos'].x)
            axis='y'
        elif axis=='y':
            obj.sort(key=lambda a: a['pos'].y)
            axis='x'
        left=obj[:len(obj)//2:1]
        right=obj[len(obj)//2::1]
        return [fullmap.bvh(left,axis),fullmap.bvh(right,axis)] #split it out
    @staticmethod
    def boundary(a): # we need boundaries to see if it can collide
        if type(a)==dict: # end node huh
            return {'x':[a['pos'].x-a['rad'],a['pos'].x+a['rad']],'y':[a['pos'].y-a['rad'],a['pos'].y+a['rad']]}
        l=fullmap.boundary(a[0])
        r=fullmap.boundary(a[1])
        return {'x':[min(l['x'][0],r['x'][0]),max(l['x'][1],r['x'][1])],'y':[min(l['y'][0],r['y'][0]),max(l['y'][1],r['y'][1])]} # use the component one instead
    @staticmethod
    def overlap(a,b):
        if type(a)==dict and type(b)==dict: # end node need more accuracy tho
            dst = PVector.sub(a['pos'],b['pos']).mag()
            return dst<a['rad']+b['rad']
        l=fullmap.boundary(a)
        r=fullmap.boundary(b)
        if r['x'][0]<l['x'][0]: # if r?l??
            r,l=l,r # l?r??
        if r['x'][0]>l['x'][1]: # llrr
            return False
        if r['y'][0]<l['y'][0]: # "
            r,l=l,r
        if r['y'][0]>l['y'][1]: # "
            return False
        return True # well no way it can't collide left lrlr in both axis
    @staticmethod
    def collision(bvh): # bla bla bla, code is in the Internet, just google it.
        if len(bvh)==0:
            return []
        if type(bvh)==dict:
            return []
        a=bvh[0]
        b=bvh[1]
        if fullmap.overlap(a,b):
            if type(a)==dict and type(b)==dict:
                return [[a,b]]
            if type(a)==dict:
                return fullmap.collision(b)+fullmap.collision([a,b[0]])+fullmap.collision([a,b[1]])
            if type(b)==dict:
                return fullmap.collision(a)+fullmap.collision([b,a[0]])+fullmap.collision([b,a[1]])
            return fullmap.collision(a)+fullmap.collision(b)+fullmap.collision([a[0],b[0]])+fullmap.collision([a[0],b[1]])+fullmap.collision([a[1],b[0]])+fullmap.collision([a[1],b[1]])
        else:
            return fullmap.collision(a)+fullmap.collision(b)
# for real HTTP implementation, Nope I won't do it
