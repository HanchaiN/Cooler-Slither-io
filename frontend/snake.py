# Piyanuch Anantakijsopol, Hanchai Nonprasart

import pygame,sys,random
from pygame.math import Vector2
import math

def _draw_jelly(surf,x,y,r,scale=1):
	graphic=pygame.transform.smoothscale(jelly,(int(2*r*scale),int(2*r*scale)))
	color=pygame.Color(128,192,225,0) # pygame.transform.average_color(graphic)
	slot=pygame.draw.circle(surf,color,(Vector2(x,y)+Vector2(1000,1000))*scale,r*scale)
	surf.blit(graphic,slot)
def _draw_node(surf,x,y,r,a,scale=1,head=False):
	global head_right, head_up, head_left, head_down, body
	graphic=body
	if head:
		if a<math.pi*1/2:
			graphic=head_right
		elif a<math.pi*2/2:
			graphic=head_up
		elif a<math.pi*3/2:
			graphic=head_left
		elif a<math.pi*4/2:
			graphic=head_down
	graphic=pygame.transform.smoothscale(graphic,(int(2*r*scale),int(2*r*scale)))
	graphic=pygame.transform.rotate(graphic,a*180/math.pi)
	color=pygame.Color(225,192,128,0)
	slot=pygame.draw.circle(surf,color,(Vector2(x,y)+Vector2(1000,1000))*scale,r*scale)
	surf.blit(graphic,slot)
def _draw_slither(surf,nodes,scale=1):
	for i in nodes[-1:0:-1]:
		_draw_node(surf,i['pos'][0],i['pos'][1],i['rad'],i['angle'],scale)
	_draw_node(surf,nodes[0]['pos'][0],nodes[0]['pos'][1],nodes[0]['rad'],nodes[0]['angle'],scale,head=True)
def draw(data,scale=1):
	r=data['r']*scale
	pos=(Vector2(0,0)+Vector2(r,r))
	surf=pygame.Surface((int(2*r),int(2*r)))
	pygame.draw.circle(surf,(192,192,192,255),pos,r)
	for i in data['pallets']:
		_draw_jelly(surf,data['pallets'][i]['pos'][0],data['pallets'][i]['pos'][1],data['pallets'][i]['rad'],scale)
	for i in data['slithers']:
		if data['slithers'][i]['embed']['status']!='live':
			continue
		_draw_slither(surf,data['slithers'][i]['data']['nodes'],scale)
	return surf
body=None
jelly=None
head_up=None
head_down=None
head_left=None
head_right=None
def init():
	global jelly, head_up, head_down, head_left, head_right, body
	# screen
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	pygame.display.set_caption('Cooler Slither io')
	jelly=pygame.image.load('Graphics/Yelly3.PNG')
	head_up=pygame.image.load('Graphics/head_up.PNG')
	head_down=pygame.image.load('Graphics/head_down.PNG')
	head_left=pygame.image.load('Graphics/head_left.PNG')
	head_right=pygame.image.load('Graphics/head_right.PNG')
	body=pygame.image.load('Graphics/body.PNG')
	# clock
	clock = pygame.time.Clock()
	#pygame.mixer.pre_init(44100,-16,2,512)
	return screen, clock

if __name__=='__main__': # test function here
	pass