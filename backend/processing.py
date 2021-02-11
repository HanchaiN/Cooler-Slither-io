# Hanchai Nonprasart

# I will just implement what I might need now, others will be implemented later if I want
# for infomations goto https://py.processing.org/reference
# Math
## PVector
class PVector:
	def __init__(self,x=0,y=0,z=0): # we only use 2D but just in case
		self.x=x
		self.y=y
		self.z=z
	
	def __str__(self):
		return str((self.x,self.y,self.z))
	
	def set(self,x,y=None,z=None):
		if type(x)==list:
			self.set(*list)
			return
		elif z:
			pass
		elif y:
			z=self.z
		else:
			y=x
			x=self.x
		self.x,self.y,self.z=x,y,z
	def copy(self):
		return PVector(self.x,self.y,self.z)
	def mag(self):
		return sqrt(self.magSq())
	def magSq(self):
		return sq(self.x)+sq(self.y)+sq(self.z)
	def normalize(self):
		s=PVector.div(self,self.mag())
		self.x,self.y,self.z=s.x,s.y,s.z
	def limit(self,max_):
		self.setMag(max_)
	def setMag(self,len_):
		self.normalize()
		s=PVector.mult(self,len_)
		self.x,self.y,self.z=s.x,s.y,s.z
	def heading(self):
		return atan2(self.y,self.x)
	def rotate(self,theta):
		m,a=self.mag(),self.heading()
		a+=theta
		s=PVector.fromAngle(a)
		self.x,self.y,self.z=s.x,s.y,s.z
		self.setMag(m)
	def lerp(self,x,y,z=None,amt=None):
		if not amt:
			self.lerp(x.x,x.y,x.z,y)
			return
		self.x=lerp(self.x,x,amt)
		self.y=lerp(self.y,y,amt)
		self.z=lerp(self.z,z,amt)
	@staticmethod
	def add(v1,v2):
		return PVector(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)
	@staticmethod
	def sub(v1,v2):
		return PVector.add(v1,PVector.mult(v2,-1))
	@staticmethod
	def mult(v,n):
		return PVector(v.x*n,v.y*n,v.z*n)
	@staticmethod
	def div(v,n):
		return PVector.mult(v,1/n)
	@staticmethod
	def dist(v1,v2):
		return PVector.sub(v1,v2).mag()
	@staticmethod
	def dot(v1,v2):
		return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z
	@staticmethod
	def random2D():
		return PVector.fromAngle(random(TWO_PI))
	@staticmethod
	def fromAngle(angle):
		return PVector(cos(angle),sin(angle))
## Calculation
## Trigonometry # some of them was in math
from math import ceil,exp,floor,log,pow,sqrt,acos,asin,atan,atan2,cos,degrees,radians,sin,tan
from math import dist as norm
def constrain(amt, low, high):
	return min(max(amt,low),high)
def dist(*args):
	return norm(args[:len(args)//2:],args[len(args)//2::])
def lerp(start, stop, amt):
	return map(amt, 0, 1, start, stop)
def mag(x, y):
	return dist(0, 0, x, y)
def map(value, start1, stop1, start2, stop2):
	return (value - start1) / (start1 - stop1) * (start2 - stop2) + start2
def norm(value,start, stop):
	return map(value, start, stop, 0, 1)
def sq(n):
	return n * n
## Random
import random as rnd
def randomSeed(seed):
	rnd.seed(seed)
def random(lim1,lim2=None):
	if not lim2:
		lim2=lim1
		lim1=0
	return rnd.uniform(lim1,lim2)
def randomGaussian():
	return rnd.gauss(0,1)
# Constants
from math import pi as PI
from math import tau as TAU
TWO_PI=TAU
HALF_PI=PI/2
QUARTER_PI=PI/4