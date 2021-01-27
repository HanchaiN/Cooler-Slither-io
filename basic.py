class pallet: # this part is from https://thecodingtrain.com/CodingChallenges/032.1-agar.html
    def __init__(self,pos,rad):
        self.pos=pos
        self.rad=rad
    def consume(self,vol): # this was changed a bit, since I will use the map to detect the collision by theirself
        sum = self.rad * self.rad + vol
        self.rad = sqrt(sum)
class node(pallet): # this was modified segment from https://thecodingtrain.com/CodingChallenges/064.2-inverse-kinematics.html
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
        p.setMag(self.node.rad+100/30) # the real point that follow us is tail (which actually more head and was not shown) of the head and 100 is just speed in px/s, btw since it was very laggy, I will assume the framerate to be constant at 30 or in the real server : this is 1/delta for delta as period between tick of the server
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
