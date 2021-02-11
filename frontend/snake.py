# Piyanuch Anantakijsopol

import pygame,sys,random
from pygame.math import Vector2
class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)
		self.new_block = False

		self.head_up = pygame.image.load('resources/images/h.up.png').convert_alpha()
		self.head_down = pygame.image.load('resources/images/h.d.png').convert_alpha()
		self.head_right = pygame.image.load('resources/images/h.r.png').convert_alpha()
		self.head_left = pygame.image.load('resources/images/h.l.png').convert_alpha()
		
		self.tail_up = pygame.image.load('resources/images/t.up.png').convert_alpha()
		self.tail_down = pygame.image.load('resources/images/t.d.png').convert_alpha()
		self.tail_right = pygame.image.load('resources/images/t.r.png').convert_alpha()
		self.tail_left = pygame.image.load('resources/images/t.l.png').convert_alpha()
		
		self.body_vertical = pygame.image.load('resources/images/body.png').convert_alpha()
		self.body_horizontal = pygame.image.load('resources/images/body.non.png').convert_alpha()
		
		self.body_tr = pygame.image.load('resources/images/down.r.png').convert_alpha()
		self.body_tl = pygame.image.load('resources/images/down.l.png').convert_alpha()
		self.body_br = pygame.image.load('resources/images/up.r.png').convert_alpha()
		self.body_bl = pygame.image.load('resources/images/up.l.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('resources/audio/....')
