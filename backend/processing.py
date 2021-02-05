# I will just implement what I might need now, others will be implemented later if I want
# for infomations goto https://py.processing.org/reference
# Math
## PVector
class PVector:
    def __init__(self,x=0,y=0,z=0): # we only use 2D but just in case
        self.x=x
        self.y=y
        self.z=z
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
    def normalize(self,target=None):
        if target:
            target=PVector.div(self,self.mag())
            return
        self=PVector.div(self,self.mag())
    def limit(self,max_):
        self.setMag(max_)
    def setMag(self,len_,tar_=None):
        if tar_:
            len_,tar_=tar_,len_
        else:
            tar_=self
        PVector.mult(self.normalize(),len_,tar_)
    def heading(self):
        return atan2(self.y,self.x)
    def rotate(self,theta):
        m,a=self.mag(),self.heading()
        a+=theta
        self=PVector.fromAngle(a)
        self.setMag(m)
    def lerp(self,x,y,z=None,amt=None):
        if not amt:
            self.lerp(x.x,x.y,x.z,y)
            return
        self.x=lerp(self.x,x,amt)
        self.y=lerp(self.y,y,amt)
        self.z=lerp(self.z,z,amt)
    @staticmethod
    def add(v1,v2,target=None):
        if target:
            target=PVector.add(v1,v2)
            return
        return PVector(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)
    @staticmethod
    def sub(v1,v2,target=None):
        return PVector.add(v1,PVector.mult(v2,-1),target)
    @staticmethod
    def mult(v,n,target=None):
        if target:
            target=PVector.mult(v,n)
            return
        return PVector(v.x*n,v.y*n,v.z*n)
    @staticmethod
    def div(v,n,target=None):
        return PVector.mult(v,1/n,target)
    @staticmethod
    def dist(v1,v2):
        return PVector.sub(v1,v2).mag()
    @staticmethod
    def dot(v1,v2):
        return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z
    @staticmethod
    def random2D(target=None):
        if target:
            target=PVector.random2D()
            return
        return PVector.fromAngle(random(TWO_PI))
    @staticmethod
    def fromAngle(angle, target=None):
        if target:
            target=PVector.fromAngle(angle)
            return
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