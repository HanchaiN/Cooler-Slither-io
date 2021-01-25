class pallet: # this part is from thecodingtrain.com/CodingChallenges/032.1-agar.html
    def __init__(self,pos,rad):
        self.pos=pos
        self.rad=rad
    def show(self):
        fill(0) # very bad color for the pallet
        noStroke()
        circle(self.pos.x,self.pos.y,2*self.rad)
    def consume(self,vol): # this was changed a bit, since I will use the map to detect the collision by theirself
        sum = self.rad * self.rad + vol
        self.rad = sqrt(sum)
class node(pallet): # this was modified segment from thecodingtrain.com/CodingChallenges/064.2-inverse-kinematics.html
    def __init__(self,head,rad):
        self.child=False # we will use it later
        self.angle=0 # some default value that doesn't matter
        if isinstance(head,node): # if head was a node
            self.parent=head # I don't think it have any usage, for now
            pos=self.parent.tail.copy() # of cause, we should start at their tail
        else:
            self.parent=False
            pos=head
        pallet.__init__(self,pos,rad) # and this was the pallet, once ago
        self.tail=self.pos # just dummy, doesn't matter
        self.findend() # calculation time
    def findend(self): # forward kinematics
        unit = PVector.fromAngle(self.angle)
        self.tail=PVector.add(self.pos,PVector.mult(unit,self.rad))
    def follow(self,pos): # inverse kinematics
        direction = PVector.sub(pos,self.pos) # find translation vector
        if direction.mag()==0: # if we're at it
            return # just skip
        self.angle = direction.heading() # now where did it point at
        direction.setMag(self.rad) # this is how our segment pointing from its start to end
        self.pos = PVector.sub(pos,direction) # we have to be aware that the position of the tail is at the target, not the head.
    def update(self): # updating time
        if self.child:
            self.follow(self.child.pos) # syncronize that we're right in our tract
        self.findend() # and recalculate our endpoint
    def show(self): # again but with other color
        fill(255)
        stroke(0)
        strokeWeight(1)
        circle(self.pos.x,self.pos.y,2*self.rad)
class tentacle: # our full slither are ready
    def __init__(self,pos,rad,length):
        self.vol=0 # we will record your volume as score but we dont want PI term in our way
        self.n=length # we need to know how long we are
        root=node(pos,map(0,0,self.n,rad*2,rad*3)) # of cause, our first node (the tail) and rad*2,rad*3 in size is just the optimize for better(?) looks
        self.vol+=root.rad*root.rad # update the volume
        for i in range(self.n-1):
            branch=node(root,map(i+1,0,self.n,rad*2,rad*3)) # ready for the next (previous) node and again the same rad*2,rad*3 in size is just the optimize for better(?) looks
            root.child=branch # and remember it
            root=branch # then change our view
            self.vol+=root.rad*root.rad # update the volume
        self.node=root # and remember just our head
        self.angle=0 # and again dummy initial value
    def consume(self,vol):
        # vol=sum((2*rad+i*rad/n)**2 ,i=0,n-1)
        # vol=sum((2*rad)**2+(i*rad/n)**2+(2*rad)(i*rad/n) ,i=0,n-1)
        # vol=sum((2*rad)**2, i=0,n-1)+sum((i*rad/n)**2, i=0,n-1)+sum((2*rad)(i*rad/n) ,i=0,n-1)
        # vol=n*4*rad**2+(n-1)(2n-1)rad**2 /6n + rad**2*(n-1)
        # vol=rad**2(n*4+(n-1)(2n-1)/6n + (n-1))
        # vol=rad**2(n*4+n/3-0.5+1/6n + n-1)
        # vol=rad**2(16*n/3-1.5+1/6n)
        self.vol+=vol # update score that not messed up
        rad=sqrt(self.vol/(16*self.n/3-1.5+1/(6*self.n)))
        if rad>35: # here lies your check mark optimized
            self.n+=1
            rad=sqrt(self.vol/(16*self.n/3-1.5+1/(6*self.n)))
            head=node(self.node,map(self.n-1,0,self.n,rad*2,rad*3))
            self.node.child=head
            head.pos=self.node.pos
            self.node=head # new official node congraturation
        j=self.n-1
        for i in self:
            i.consume(map(j,0,self.n,rad*2,rad*3)**2-i.rad**2)
            j-=1
    def update(self): # bigger update time
        p=PVector.fromAngle(self.angle) # unit vector for fun
        p.setMag(self.node.rad+100/frameRate) # the real point that follow us is tail (which actually more head and was not shown) of the head and 100 is just speed in px/s
        p=PVector.add(self.node.pos,p) # and add it from current position
        self.node.follow(p) # follow our node
        for i in self: # this use iterator that will explain below
            i.update() # update each node from head to tail
    def __iter__(self): # how to use this as iterator
        self.iteration=self.node # create variable to remeber where we are
        self.ind=-1 # and which node is this
        return self
    def next(self):
        if not self.ind==-1: # except for the first one
            self.iteration = self.iteration.parent # we will move to the next one
        self.ind+=1 # just to escape form the first indicator actually
        if not self.iteration: # if nothing is avaliable
            raise StopIteration # we end the iteration
        return self.iteration # and return what we got
class bot(tentacle):
    def __init__(self,pos,rad,length):
        tentacle.__init__(self,pos,rad,length)
        self.wgood=random(0,2) # will be optimize later
        self.wbad=random(-2,0) # will be optimize later
        self.rgood=random(0,min(width,height)/2) # will be optimize later
        self.rbad=random(0,min(width,height)/2) # will be optimize later
    def calculate(self,g,b): # how it work? well go learn this instead https://thecodingtrain.com/CodingChallenges/069.5-steering-evolution.html
        D=PVector(0,0)
        rec=self.rgood
        cls=False
        for i in g:
            d=self.node.pos.dist(i['pos'])-i['rad'];
            if d<rec:
                rec=d
                cls=i['pos']
        if cls:
            delta=PVector.sub(cls,self.node.pos)
            delta=delta.mult(self.wgood)
            D=PVector.add(D,delta)
        rec=self.rbad
        cls=False
        for i in g:
            d=self.node.pos.dist(i['pos'])-i['rad'];
            if d<rec:
                rec=d
                cls=i['pos']
        if cls:
            delta=PVector.sub(cls,self.node.pos)
            delta=delta.mult(self.wbad)
            D=PVector.add(D,delta)
        if D.mag()!=0:
            self.angle=atan2(D.y,D.x)
class fullgame: # the full server have come
    def __init__(self,radius):
        self.r=radius
        self.slithers={} # list of slither, using some IDs
        self.pallets=[] # and simply list of pallets
    def slither(self,pos,id): # spawn new slither of ID at pos
        if id in self.slithers: # sorry but this ID existed
            return False
        self.slithers[id]=tentacle(pos,25,5) # and its time to create the new one with optimized variable (size,length)
    def bot(self,pos,id):
        if id in self.slithers: # sorry but this ID existed
            return False
        self.slithers[id]=bot(pos,25,5) # and its time to create the new one with optimized variable (size,length)
    def objectlist(self): # we need to list objects for collision detection
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
        # check for collision
        # * pallet + pallet = grow -> disabled nope
        # * head + pallet = grow
        # * head + border = dead (can be called later)
        # * head + body = dead
        # and maybe some pallet movement for fun i.e. flocking behavior? If I'm not lazy tho
        col=self.collision(self.bvh(self.objectlist())) # these function will be explianed later
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
                    self.pallets.append(pallet(loc,10)) # place standard (10) pallet at somewhere that 0.2% (+-3sigma) out of the axist
            del self.slithers[i] # and it was completely removed
        for t in self.slithers:
            if isinstance(self.slithers[t],bot):
                ls=self.objectlist()
                g=[]
                b=[]
                for i in ls:
                    if i['data']['type']=='pallet':
                        g.append(i)
                    elif i['data']['type']=='slither' and i['data']['index']!=t:
                        b.append(i)
                p=self.slithers[t].node.pos.copy()
                r=p.mag()
                p.setMag(self.r+r)
                b.append({'pos':p,'rad':r})
                self.slithers[t].calculate(g,b)
            self.slithers[t].update() # update the slithers, now!
        if len(self.pallets)<100: # we didn't want to be in flood of pallets, right
            self.pallets.append(pallet(PVector.mult(PVector.random2D(),random(self.r)),10)) # this make the center have more pallet density than that of the border but different ways from when it drop from the dead (10 is that same constant btw (I may want to random it from 10(smallest) to 25(biggest limit)))
    def show(self,main=''): # some shame graphic
        if main in self.slithers: # if we focus on exist slither
            print(self.slithers[main].vol) # status export huh
            translate(width/2,height/2)
            scale(100*0.5/self.slithers[main].node.rad) # scale so that the head is of size 100 (huh)
            translate(-self.slithers[main].node.pos.x,-self.slithers[main].node.pos.y) # and make sure that  =the slither is in the center
        else: # or if you're dead you will look at the entire map aka minimap
            translate(width/2,height/2) # move the map to the center
            scale(min(width,height)*0.5/self.r) # try to fit all map inside
        stroke(255,0,0)
        strokeWeight(10)
        fill(128)
        circle(0,0,2*self.r) # don't forget the border line to warn you
        for p in self.pallets:
            p.show() # the pallets here
        for t in self.slithers:
            for i in self.slithers[t]:
                i.show() # slithers there
    @staticmethod
    def bvh(obj,axis='x'): # bounding volume hierarchy is the nice idea
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
        return [fullgame.bvh(left,axis),fullgame.bvh(right,axis)] #split it out
    @staticmethod
    def boundary(a): # we need boundaries to see if it can collide
        if type(a)==dict: # end node huh
            return {'x':[a['pos'].x-a['rad'],a['pos'].x+a['rad']],'y':[a['pos'].y-a['rad'],a['pos'].y+a['rad']]}
        l=fullgame.boundary(a[0])
        r=fullgame.boundary(a[1])
        return {'x':[min(l['x'][0],r['x'][0]),max(l['x'][1],r['x'][1])],'y':[min(l['y'][0],r['y'][0]),max(l['y'][1],r['y'][1])]} # use the component one instead
    @staticmethod
    def overlap(a,b):
        if type(a)==dict and type(b)==dict: # end node need more accuracy tho
            dst = PVector.sub(a['pos'],b['pos']).mag()
            return dst<a['rad']+b['rad']
        l=fullgame.boundary(a)
        r=fullgame.boundary(b)
        if r['x'][0]<l['x'][0]: # r?l??
            r,l=l,r # l?r??
        if r['x'][0]>l['x'][1]: # llrr
            return False
        if r['y'][0]<l['y'][0]: # "
            r,l=l,r
        if r['y'][0]>l['y'][1]: # "
            return False
        return True # well no way it can't collide left
    @staticmethod
    def collision(bvh): # bla bla bla, code is in the Internet, just google it.
        if type(bvh)==dict:
            return []
        a=bvh[0]
        b=bvh[1]
        if fullgame.overlap(a,b):
            if type(a)==dict and type(b)==dict:
                return [[a,b]]
            if type(a)==dict:
                return fullgame.collision(b)+fullgame.collision([a,b[0]])+fullgame.collision([a,b[1]])
            if type(b)==dict:
                return fullgame.collision(a)+fullgame.collision([b,a[0]])+fullgame.collision([b,a[1]])
            return fullgame.collision(a)+fullgame.collision(b)+fullgame.collision([a[0],b[0]])+fullgame.collision([a[0],b[1]])+fullgame.collision([a[1],b[0]])+fullgame.collision([a[1],b[1]])
        else:
            return fullgame.collision(a)+fullgame.collision(b)
g=fullgame(5000) # let make a server
def setup():
    global g # idk if this is necessary but game is global variable
    size(500,500) # screen size
    # g.slither(PVector(0,0),'Player') # you
    g.bot(PVector(-500,0),'P') # test npc
    frameRate(30) # for some smoother(?) animation
def draw():
    global g # idk if this is necessary but game is global variable
    if 'Player' not in g.slithers: # you died
        pass
        # return # but I cancled it
    background(255,128,128) # just bad died graphic
    g.show('Player') # Let try to focus on our slither
    if 'Player' in g.slithers: # instead if the player died we just skip 
        p=PVector(mouseX-width/2,mouseY-height/2)
        g.slithers['Player'].angle=p.heading() # updating the slither
    g.update() # then we update the map
# look as this, it works. Except from some of the cooler feature like Pallet movements
# I will reupload later so please be aware
# for pallets I may skip or use https://thecodingtrain.com/CodingChallenges/124-flocking-boids.html
