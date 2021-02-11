# Hanchai Nonprasart

import pickle # just dumb it
import json
import time # to track ticks per sec

from processing import * # to implement used processing built-in functions in normal cpython

class _pallet: # this part is from https://thecodingtrain.com/CodingChallenges/032.1-agar.html
	def __init__(self,pos,rad):
		if not pos.x:
			raise(Exception())
		self.__pos=pos
		self.__rad=rad
	def consume(self,vol,pos=None): # this was changed a bit, since I will use the map to detect the collision by theirself
		sum = self.__rad * self.__rad + vol
		if pos: # if we given the final position
			self.__pos.lerp(pos,vol/sum)# longest line huh, this lead new pallet to be at position between the old one weighted by their volume
		self.__rad = sqrt(sum)
	def data(self):
		return {'pos':[self.__pos.x,self.__pos.y],'rad':self.__rad}
	def __str__(self):
		return json.dumps(self.data())
class _node: # this was modified segment from https://thecodingtrain.com/CodingChallenges/064.2-inverse-kinematics.html
	def __init__(self,head,rad):
		self.__child=None # we will use it later
		self.__angle=0 # some default value that doesn't matter
		if isinstance(head,_node): # if head was a node
			self.__parent=head # I don't think it have any usage, for now
			pos=self.__parent.__tail.copy() # of cause, we should start at their tail
		else:
			self.__parent=None
			pos=head
		self.__pos=pos # Duplicated from _pallet
		self.__rad=rad # Duplicated from _pallet
		self.__tail=self.__pos # just dummy, doesn't matter
		self.__findend() # calculation time
	def consume(self,vol,pos=None): # Duplicated from _pallet
		sum = self.__rad * self.__rad + vol
		if pos: # if we given the final position
			self.__pos.lerp(pos,vol/sum)
		self.__rad = sqrt(sum)
	def data(self): # Duplicated from _pallet
		return {'pos':[self.__pos.x,self.__pos.y],'angle':self.__angle,'rad':self.__rad}
	def __findend(self): # forward kinematics
		self.__tail=PVector.add(self.__pos,PVector.mult(PVector.fromAngle(self.__angle),self.__rad))
	def follow(self,pos): # inverse kinematics
		direction = PVector.sub(pos,self.__pos) # find translation vector
		if direction.mag()==0: # if we're at it
			return # just skip
		self.__angle = direction.heading() # now where did it point at
		direction.setMag(self.__rad) # this is how our segment pointing from its start to end
		self.__pos = PVector.sub(pos,direction) # we have to be aware that the position of the tail is at the target, not the head.
	def setchild(self,child):
		self.__child=child
		self.__pos=PVector(*self.__child.data()['pos'])
		self.__child.setparent(self)
	def setparent(self,parent):
		self.__parent=parent
		self.__pos=PVector(*self.__parent.data()['pos'])
	def getparent(self):
		return self.__parent
	def update(self): # updating time
		if self.__child:
			self.follow(PVector(*self.__child.data()['pos'])) # syncronize that we're right in our tract
		self.__findend() # and recalculate our endpoint
	def __str__(self):
		return json.dumps(self.data())
class _tentacle: # our full slither are ready
	def __init__(self,pos,rad,length):
		self.__vol=0 # we will record your volume as score but we dont want PI term in our way
		self.__n=length # we need to know how long we are
		root=_node(pos,map(0,0,self.__n,rad*2,rad*3)) # of cause, our first node (the tail) and rad*2,rad*3 in size is just the optimize for better(?) looks
		self.__vol+=root.data()['rad']*root.data()['rad'] # update the volume
		for i in range(self.__n-1):
			branch=_node(root,map(i+1,0,self.__n,rad*2,rad*3)) # ready for the next (previous) node and again the same rad*2,rad*3 in size is just the optimize for better(?) looks
			root.setchild(branch) # and remember it
			root=branch # then change our view
			self.__vol+=root.data()['rad']*root.data()['rad'] # update the volume
		self.__node=root # and remember just our head
		self.__angle=0 # and again dummy initial value
	def consume(self,vol):
		# vol=sum((2*rad+i*rad/n)**2 ,i=0,n-1)
		# vol=sum((2*rad)**2+(i*rad/n)**2+(2*rad)(i*rad/n) ,i=0,n-1)
		# vol=sum((2*rad)**2, i=0,n-1)+sum((i*rad/n)**2, i=0,n-1)+sum((2*rad)(i*rad/n) ,i=0,n-1)
		# vol=n*4*rad**2+(n-1)(2n-1)rad**2 /6n + rad**2*(n-1)
		# vol=rad**2(n*4+(n-1)(2n-1)/6n + (n-1))
		# vol=rad**2(n*4+n/3-0.5+1/6n + n-1)
		# vol=rad**2(16*n/3-1.5+1/6n)
		self.__vol+=vol # update score that not messed up
		rad=sqrt(self.__vol/(16*self.__n/3-1.5+1/(6*self.__n)))
		if rad>35: # here lies your check mark optimized
			self.__n+=1
			rad=sqrt(self.__vol/(16*self.__n/3-1.5+1/(6*self.__n)))
			head=_node(self.__node,map(self.__n-1,0,self.__n,rad*2,rad*3))
			self.__node.setchild(head)
			self.__node=head # new official node congraturation
		j=self.__n-1
		for i in self:
			i.consume(map(j,0,self.__n,rad*2,rad*3)**2-i.data()['rad']**2)
			j-=1
	def update(self,dt): # bigger update time
		p=PVector.fromAngle(self.__angle) # unit vector for fun
		p.setMag(self.__node.data()['rad']+100*dt) # the real point that follow us is tail (which actually more head and was not shown) of the head and 100 is just speed in px/s
		p=PVector.add(PVector(*self.__node.data()['pos']),p) # and add it from current position
		self.__node.follow(p) # follow our node
		for i in self: # this use iterator that will explain below
			i.update() # update each node from head to tail
	def setangle(self,angle):
		self.__angle=angle
	def __iter__(self): # how to use this as iterator
		self.__iteration=self.__node # create variable to remeber where we are
		self.__ind=-1 # and which node is this
		return self
	def __next__(self):
		if self.__ind!=-1: # except for the first one
			self.__iteration = self.__iteration.getparent() # we will move to the next one
		self.__ind+=1 # just to escape form the first indicator actually
		if not self.__iteration: # if nothing is avaliable
			raise StopIteration # we end the iteration
		return self.__iteration # and return what we got
	def head(self):
		return self.__node
	def data(self):
		return {'vol':self.__vol,'nodes':[i.data() for i in self]}
	def __str__(self):
		return json.dumps(self.data())

class fullmap: # the full server have come
	def __init__(self,radius):
		self.r=radius
		self.__slithers={} # list of slither, using some IDs
		self.__slithers_data={}
		self.__pallets={} # and simply list of pallets
		self.t=time.time_ns()
		self.dt=0
	def spawn(self,data={}): # spawn new slither of ID at pos
		i=1
		while i in self.__slithers:
			i+=1
		pos=PVector.mult(PVector.random2D(),self.r*random(0.2,0.8)) # wish you have lucky spawn
		self.__slithers[i]=_tentacle(pos,25,5) # and its time to create the new one with optimized variable (size,length)
		self.__slithers_data[i]=data
		self.__slithers_data[i]['public']['status']='live'
		self.__slithers_data[i]['private']['delete']=False
		return i
	def remove(self,iden):
		if iden in self.__slithers and self.__slithers_data[iden]['public']['status']=='dead':
			del self.__slithers[iden]
			del self.__slithers_data[iden]
			return True
		if iden in self.__slithers:
			self.__slithers_data[iden]['private']['delete']=not self.__slithers_data[iden]['private']['delete']
			return True
		return False
	def __create(self,loc,size=10):
		i=1
		while i in self.__pallets:
			i+=1
		self.__pallets[i]=_pallet(loc,size) # put new pallet in at standard size of 10
	def __objectlist(self): # we need to list objects for collision detection
		objects=[]
		for i in self.__pallets:
			objects.append(self.__pallets[i].data())
			objects[-1].update({'data':{'type':'pallet','index':i}})
		for i in self.__slithers:
			if self.__slithers_data[i]['public']['status']=='dead':
				continue
			j=0
			for n in self.__slithers[i]:
				objects.append(n.data())
				objects[-1].update({'data':{'type':'slither','index':i,'location':j}})
				j+=1
		return objects # well I just include all object in the game one-by-one
	def update(self): # again updating time aka update()
		event={}
		col=_bvh(self.__objectlist()).collisions() # these function will be explianed later
		dead=set([]) # we need to track for the dead one
		eaten=set([]) # and also the eaten pallet
		for i in col: # check each (detected) collision
			i.sort(key=lambda x:x['data']['type']) # for my hand's health (which was gone long ago) we will eliminate some useless choices by arrange the type of objects
			if i[0]['data']['type']=='pallet':
				if i[1]['data']['type']=='pallet':
					if self.__pallets[i[1]['data']['index']].data()['rad']<35 and not(i[0]['data']['index'] in eaten or i[1]['data']['index'] in eaten): # pallet and pallet will merge but to avoid oversize (25++ I guess) and lost of volume : we have this condition
						eaten.add(i[0]['data']['index']) # mark as eaten
						self.__pallets[i[1]['data']['index']].consume(self.__pallets[i[0]['data']['index']].data()['rad']**2,PVector(*self.__pallets[i[0]['data']['index']].data()['pos'])) # time to consume (and as I said we ignored PI
				elif i[1]['data']['type']=='slither':
					if i[1]['data']['location']==0 and not i[0]['data']['index'] in eaten: # to avoid double eating and to make sure that it was eated from the head
						eaten.add(i[0]['data']['index']) # bla bla bla same as previous one
						self.__slithers[i[1]['data']['index']].consume(self.__pallets[i[0]['data']['index']].data()['rad']**2)
				else:
					pass # this not suppose to exist for now
			elif i[0]['data']['type']=='slither':
				if i[1]['data']['type']=='slither':
					i.sort(key=lambda x:x['data']['location']) # again
					if i[0]['data']['index']!=i[1]['data']['index'] and i[0]['data']['location']==0 and i[1]['data']['location']==0: # to not eat itself and to make sure that it was hitted at the head
						dead.add(i[0]['data']['index']) # now he's dead
				else:
					pass # again
			else:
				pass # again
		for i in self.__pallets: # idk how but the pallet drop out side the map
			if PVector(*self.__pallets[i].data()['pos']).mag()>self.r-self.__pallets[i].data()['rad']:
				eaten.add(i) # boom the border eated you 555
		eaten=list(eaten) # list eaten pallet
		for i in eaten:
			self.__pallets.pop(i) # pop the pallet gone
		for i in self.__slithers: # check if it dead by the border
			if self.__slithers_data[i]['public']['status']!='dead':
				if PVector(*self.__slithers[i].head().data()['pos']).mag()>self.r-self.__slithers[i].head().data()['rad']:
					dead.add(i) # boom
				if self.__slithers[i].data()['vol']>(self.r)**2:
					self.__slithers_data[i]['public']['status']='win' # congrats here
					if 'win' in event:
						event['win'].add(self.__slithers_data[i]['private']['username'])
					else:
						event['win']=set([self.__slithers_data[i]['private']['username']])
		dead=list(dead)
		for i in dead: # again but we have to care about drop
			for n in self.__slithers[i]: # this make server crash so I change to just a big drop
				k=(randomGaussian()+1)**2+n.data()['rad']*n.data()['rad']
				loc=PVector(randomGaussian(),randomGaussian())
				loc=PVector.mult(loc,n.data()['rad']/3)
				loc=PVector.add(loc,PVector(*n.data()['pos']))
				self.__create(loc,sqrt(k))
				# k=randomGaussian()+n.data()['rad']*n.data()['rad'] # drop random amount for the volume about the dead node
				# k/=10*10 # and divided by the size of new pallet (10 I guess)
				# if k<0:
				# 	k=0 # make sure that no error from k<0
				# k=floor(k) # and from k not integer
				# for j in range(k):
				# 	loc=PVector(randomGaussian(),randomGaussian())
				# 	loc=PVector.mult(loc,n.data()['rad']/3)
				# 	loc=PVector.add(loc,PVector(*n.data()['pos']))
				# 	self.__create(loc) # place standard pallet at somewhere that 0.2% (+-3sigma) out of the axist
			self.__slithers_data[i]['public']['status']='dead' # to notify user
			self.__slithers_data[i]['private']['dead']=self.t+1*60*10**9 # time to delete this dead from server
			if self.__slithers_data[i]['private']['delete']:
				self.remove(i)
		dead=set([])
		for t in self.__slithers:
			if self.__slithers_data[t]['public']['status']=='dead':
				if self.t>self.__slithers_data[t]['private']['dead']: # If you don't delete in given time, we will do it for you
					dead.add(t)
				continue
			self.__slithers[t].update(self.dt) # update the slithers, now!
		for t in dead:
			self.remove(t)
		if len(self.__pallets)<0.2*(self.r/10)**2: # we didn't want to be in flood of pallets, right so let say 0.2 of the area
			self.__create(PVector.mult(PVector.random2D(),random(self.r))) # this make the center have more pallet density than that of the border but different ways from when it drop from the dead
		self.dt=0.5*self.dt+0.5*10**(-9)*(time.time_ns()-self.t)
		self.t=time.time_ns()
		return 1/self.dt,event
	def turn(self,iden,angle): # anyone with ID can turn the slither to that angle
		if iden in self.__slithers and self.__slithers_data[i]['public']['status']!='dead':
			self.__slithers[iden].setangle(angle)
			return True
		return False
	def export(self): # all data of all user is here tho, so hacks is possible if you don't apply some filter
		d={'r':self.r,'slithers':{},'pallets':{}}
		for p in self.__pallets:
			d['pallets'][p]=self.__pallets[p].data()
		for t in self.__slithers:
			d['slithers'][t]={'data':self.__slithers[t].data(),'embed':self.__slithers_data[t]['public']}
		return d
	def store(self): # take this
		pickle.dumb(self,open('save.bin','wb')) # I'm too lazy to modify this to json and then import back, so I just dump it all
	@staticmethod
	def load(): # and pick this
		return pickle.load(open('save.bin','rb'))
	def __str__(self):
		return json.dumps(self.export())

class _bvh:
	def __init__(self,objects,axis='x'):
		self.l=None
		self.r=None
		self.n=None
		self.hitbox=None
		if len(objects)==0:
			return
		if len(objects)==1: # end node now
			self.n=objects[0]
			return
		if axis=='x':
			objects.sort(key=lambda a: a['pos'][1])
			axis='y'
		elif axis=='y':
			objects.sort(key=lambda a: a['pos'][0])
			axis='x'
		self.l=_bvh(objects[:len(objects)//2:1],axis)
		self.r=_bvh(objects[len(objects)//2::1],axis)
	def boundary(self): # we need boundaries to see if it can collide
		if not self.hitbox:
			if self.n: # end node huh
				return {'x':[self.n['pos'][0]-self.n['rad'],self.n['pos'][0]+self.n['rad']],'y':[self.n['pos'][1]-self.n['rad'],self.n['pos'][1]+self.n['rad']]}
			l=self.l.boundary()
			r=self.r.boundary()
			self.hitbox={'x':[min(l['x'][0],r['x'][0]),max(l['x'][1],r['x'][1])],'y':[min(l['y'][0],r['y'][0]),max(l['y'][1],r['y'][1])]} # use the component one instead
		return self.hitbox # dynamic programming, kind of
	@staticmethod
	def overlap(a,b):
		if a.n and b.n: # end node need more accuracy tho
			dst = PVector.sub(PVector(*a.n['pos']),PVector(*b.n['pos'])).mag()
			return dst<a.n['rad']+b.n['rad']
		l=a.boundary()
		r=b.boundary()
		if r['x'][0]<l['x'][0]: # if r?l??
			r,l=l,r # l?r??
		if r['x'][0]>l['x'][1]: # llrr
			return False
		if r['y'][0]<l['y'][0]: # "
			r,l=l,r
		if r['y'][0]>l['y'][1]: # "
			return False
		return True # well no way it can't collide left # lrlr in both axis
	def collisions(self):
		if self.n:
			return []
		return self.collision(self.l,self.r)
	@staticmethod
	def collision(a,b): # bla bla bla, code is in the Internet, just google it.
		if (not a or not b):
			return []
		if _bvh.overlap(a,b):
			if a.n and b.n:
				return [[a.n,b.n]]
			if a.n:
				return b.collisions()+_bvh.collision(a,b.l)+_bvh.collision(a,b.r)
			if b.n:
				return a.collisions()+_bvh.collision(b,a.l)+_bvh.collision(b,a.r)
			return a.collisions()+b.collisions()+_bvh.collision(a.l,b.l)+_bvh.collision(a.l,b.r)+_bvh.collision(a.r,b.l)+_bvh.collision(a.r,b.r)
		return a.collisions()+b.collisions()
	def __str__(self):
		return f"({self.l},{self.r})" if self.l and self.r else (f"({self.n})" if self.n else "()")+f" : {self.hitbox}"