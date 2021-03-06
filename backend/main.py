# original code at https://github.com/clear-code-projects/Snake
# original code at https://techwithtim.net/tutorials/socket-programming/
# modified by Hanchai Nonprasart

import pygame,random
from pygame.math import Vector2
import socket,threading,os

class SNAKE:
	def __init__(self,i,d):
		self.i=i
		self.d=d
		self.body = [self.i]
		self.direction = Vector2(0,0) if static else self.d # choose between static mode enable or not
		self.new_block = snake_length
		self.invincible = True

		self.texture={}

		self.texture['head']={}
		self.texture['head']['standard'] = pygame.transform.smoothscale(pygame.image.load('Graphics/head_up.png').convert_alpha(), (cell_size,cell_size))
		self.texture['head']['u'] = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.texture['head']['u'] = pygame.transform.smoothscale(self.texture['head']['u'], (cell_size,cell_size))
		self.texture['head']['l'] = pygame.transform.rotate(self.texture['head']['u'],90)
		self.texture['head']['d'] = pygame.transform.rotate(self.texture['head']['l'],90)
		self.texture['head']['r'] = pygame.transform.rotate(self.texture['head']['d'],90)
		
		self.texture['tail']={}
		self.texture['tail']['u'] = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.texture['tail']['u'] = pygame.transform.smoothscale(self.texture['tail']['u'], (cell_size,cell_size))
		self.texture['tail']['l'] = pygame.transform.rotate(self.texture['tail']['u'],90)
		self.texture['tail']['d'] = pygame.transform.rotate(self.texture['tail']['l'],90)
		self.texture['tail']['r'] = pygame.transform.rotate(self.texture['tail']['d'],90)

		self.texture['body']={}
		# straight
		self.texture['body']['bt'] = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.texture['body']['bt'] = pygame.transform.smoothscale(self.texture['body']['bt'], (cell_size,cell_size))
		self.texture['body']['rl'] = pygame.transform.rotate(self.texture['body']['bt'],90)
		self.texture['body']['tb'] = pygame.transform.rotate(self.texture['body']['rl'],90)
		self.texture['body']['lr'] = pygame.transform.rotate(self.texture['body']['tb'],90)

		# counter clockwise
		self.texture['body']['bl'] = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.texture['body']['bl'] = pygame.transform.smoothscale(self.texture['body']['bl'], (cell_size,cell_size))
		self.texture['body']['rb'] = pygame.transform.rotate(self.texture['body']['bl'],90)
		self.texture['body']['tr'] = pygame.transform.rotate(self.texture['body']['rb'],90)
		self.texture['body']['lt'] = pygame.transform.rotate(self.texture['body']['tr'],90)

		# clockwise
		self.texture['body']['br'] = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.texture['body']['br'] = pygame.transform.smoothscale(self.texture['body']['br'], (cell_size,cell_size))
		self.texture['body']['rt'] = pygame.transform.rotate(self.texture['body']['br'],90)
		self.texture['body']['tl'] = pygame.transform.rotate(self.texture['body']['rt'],90)
		self.texture['body']['lb'] = pygame.transform.rotate(self.texture['body']['tl'],90)

		# u-turn
		self.texture['body']['bb'] = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.texture['body']['bb'] = pygame.transform.smoothscale(self.texture['body']['bb'], (cell_size,cell_size))
		self.texture['body']['rr'] = pygame.transform.rotate(self.texture['body']['bb'],90)
		self.texture['body']['tt'] = pygame.transform.rotate(self.texture['body']['rr'],90)
		self.texture['body']['ll'] = pygame.transform.rotate(self.texture['body']['tt'],90)
		# self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

	def draw_snake(self):

		if len(self.body)==1:
			x_pos = int(self.body[0].x * cell_size)
			y_pos = int(self.body[0].y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
			if -self.d == Vector2(1,0): relation='l'
			elif -self.d == Vector2(-1,0): relation='r'
			elif -self.d == Vector2(0,1): relation='u'
			elif -self.d == Vector2(0,-1): relation='d'
			game.blit(self.texture['head'][relation],block_rect)
			# game.blit(self.texture['head']['standard'],block_rect) # sadly this image doesn't exist, yet
			return

		for index,block in list(enumerate(self.body))[::-1]:
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				head=self.body[1] - self.body[0]
				head.x%=cell_number
				head.y%=cell_number
				relation = ''
				if head == Vector2(1,0): relation='l'
				elif head == Vector2(cell_number-1,0): relation='r'
				elif head == Vector2(0,1): relation='u'
				elif head == Vector2(0,cell_number-1): relation='d'
				game.blit(self.texture['head'][relation],block_rect)
			elif index == len(self.body) - 1:
				tail=self.body[-2] - self.body[-1]
				tail.x%=cell_number
				tail.y%=cell_number
				relation = ''
				if tail == Vector2(1,0): relation='l'
				elif tail == Vector2(cell_number-1,0): relation='r'
				elif tail == Vector2(0,1): relation='u'
				elif tail == Vector2(0,cell_number-1): relation='d'
				game.blit(self.texture['tail'][relation],block_rect)
			else:
				previous_block = self.body[index + 1] - block
				previous_block.x%=cell_number
				previous_block.y%=cell_number
				next_block = self.body[index - 1] - block
				next_block.x%=cell_number
				next_block.y%=cell_number
				previous_side = ''
				if previous_block == Vector2(1,0): previous_side='r'
				elif previous_block == Vector2(cell_number-1,0): previous_side='l'
				elif previous_block == Vector2(0,1): previous_side='b'
				elif previous_block == Vector2(0,cell_number-1): previous_side='t'
				next_side = ''
				if next_block == Vector2(1,0): next_side='r'
				elif next_block == Vector2(cell_number-1,0): next_side='l'
				elif next_block == Vector2(0,1): next_side='b'
				elif next_block == Vector2(0,cell_number-1): next_side='t'
				game.blit(self.texture['body'][previous_side+next_side],block_rect)

	def move_snake(self):
		if len(self.body)>snake_length:
			self.invincible = False
		if self.direction != Vector2(0,0):
			if self.new_block==0:
				if len(self.body)<2:
					self.reset()
					return
				body_copy = self.body[:-1]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]
			elif self.new_block>0:
				if len(self.body)<1:
					self.reset()
					return
				body_copy = self.body[:]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]
				self.new_block-=1
			elif self.new_block<0:
				if len(self.body)<3:
					self.reset()
					return
				body_copy = self.body[:-2]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]
				self.new_block+=1
			else:
				pass

	def add_block(self):
		self.new_block+=1
	def remove_block(self): # no more of 1 hit dead
		self.new_block-=1

	# def play_crunch_sound(self):
	# 	self.crunch_sound.play()

	def reset(self):
		self.body = [self.i]
		if static:
			self.direction =  Vector2(0,0)
		self.new_block=snake_length
		self.invincible = True

class FRUIT:
	def __init__(self):
		self.texture = []
		self.texture.append(pygame.transform.smoothscale(pygame.image.load('Graphics/Yelly1.png').convert_alpha(), (cell_size,cell_size)))
		self.texture.append(pygame.transform.smoothscale(pygame.image.load('Graphics/Yelly2.png').convert_alpha(), (cell_size,cell_size)))
		self.texture.append(pygame.transform.smoothscale(pygame.image.load('Graphics/Yelly3.png').convert_alpha(), (cell_size,cell_size)))
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		game.blit(self.texture[self.t],fruit_rect)
		#pygame.draw.rect(game,(126,166,114),fruit_rect)

	def randomize(self):
		self.x = random.randint(1,cell_number - 2)
		self.y = random.randint(1,cell_number - 2)
		self.pos = Vector2(self.x,self.y)
		self.t=random.randint(0,len(self.texture)-1)

class MAIN:
	def __init__(self):
		self.snake = [SNAKE(Vector2(snake_length-1,snake_length-1),Vector2(1,0)),SNAKE(Vector2(cell_number-snake_length,cell_number-snake_length),Vector2(-1,0))]
		self.fruit = []
		for i in range(fruit_num):
			self.spawn_fruits()

	def update(self):
		for i in range(len(self.snake)):
			self.snake[i].move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		self.draw_grass()
		for i in range(len(self.fruit)):
			self.fruit[i].draw_fruit()
		for i in range(len(self.snake)):
			self.snake[i].draw_snake()
		self.draw_score()

	def check_collision(self):
		eaten=set([])
		for i in range(len(self.snake)):
			for j in range(len(self.fruit)):
				if self.fruit[j].pos.distance_squared_to(self.snake[i].body[0])<1:
					eaten.add(j)
					self.snake[i].add_block()
		rm=set([])
		for j in eaten:
			self.fruit[j].randomize()
			i=0
			while any(any(block.distance_squared_to(self.fruit[j].pos)<1 for block in self.snake[i].body[:]) for i in range(len(self.snake))) or any(i!=j and self.fruit[i].pos.distance_squared_to(self.fruit[j].pos)<1 for i in range(len(self.fruit))):
				self.fruit[j].randomize()
				i+=1
				if i>100:
					rm.add(j)
					break
		for i in sorted(rm)[::-1]:
			self.fruit.pop(j)
	
	def spawn_fruits(self):
		j=len(self.fruit)
		self.fruit.append(FRUIT())
		i=0
		while any(any(block.distance_squared_to(self.fruit[j].pos)<1 for block in self.snake[i].body[:]) for i in range(len(self.snake))) or any(self.fruit[i].pos.distance_squared_to(self.fruit[j].pos)<1 for i in range(j)):
			self.fruit[j].randomize()
			i+=1
			if i>100: # no food this time, sorry
				self.fruit.pop()
				return

	def check_fail(self):
		dead=set([])
		eaten=[]
		for i in range(len(self.snake)):
			if not 0 <= self.snake[i].body[0].x < cell_number or not 0 <= self.snake[i].body[0].y < cell_number:
				if random.random()<eat_rate: # mercy's here, enjoy it
					eaten.append(i) # but you still pay it
					self.spawn_fruits() # here's how we make our new fruits
					self.snake[i].body[0].update(self.snake[i].body[0].x%cell_number,self.snake[i].body[0].y%cell_number)
					continue
				dead.add(i)
		for i in range(len(self.snake)):
			for j in range(len(self.snake)):
				if i==j or self.snake[i].invincible or self.snake[j].invincible: # new-born are is invincible and you won't kill yourself in this game(modifiable)
					continue
				if i<j and self.snake[j].body[0] == self.snake[i].body[0]: # head x head
					eaten.append(i) # both get punishment
					eaten.append(j) # both get punishment
					if random.random()>eat_rate: # if we decided to punish by dead not just eat
						if random.random()>0.5: # fair game, no luck stat involve
							dead.add(j) # no price here, sorry
						else:
							dead.add(i) # no price here, sorry
					else:
						pass # no real reason why you both should get reward on this
					continue # this snake friend is done no multiple benifits if you manage to fold yourself on a single block
				for block in self.snake[j].body[1:]: # head x body
					if block == self.snake[i].body[0]: # either you eat others or you die
						if random.random()<eat_rate: # luckily you ain't dead (we may change weight by some variable)
							eaten.append(j)
							for k in range(2): # make it more convincing, and make game avaliable for playing after all fruit once cleared
								self.snake[i].add_block()
						else: # you'll be dead where you stand
							dead.add(i)
							for k in range(max(len(self.snake[j].body)+min(0,self.snake[j].new_block),0)//2): # their luck, free length
								self.snake[j].add_block()
						break # this snake friend is done no multiple benifits if you manage to fold yourself on a single block
				# check if your head happened to cross multiple friends
		for i in dead:
			self.game_over(i)
		for i in eaten:
			if i not in dead:
				self.snake[i].remove_block()
	
	def game_over(self,i):
		self.snake[i].reset()

	def draw_grass(self):
		for row in range(cell_number):
			for col in range(cell_number):
				if (row+col) % 2 == 0: 
					grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
					pygame.draw.rect(game,grass_color,grass_rect)
				else:
					grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
					pygame.draw.rect(game,low_grass,grass_rect)

	def draw_score(self):
		score_surface = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25).render(f"{len(self.snake[0].body)}:{len(self.snake[1].body)}",True,(16,32,16))
		score_rect = score_surface.get_rect(bottomright = (int(cell_size * (cell_number) - 7),int(cell_size * (cell_number))))
		jelly=pygame.transform.smoothscale(pygame.image.load('Graphics/Yelly1.png').convert_alpha(), (cell_size,cell_size))
		jelly_rect = jelly.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(jelly_rect.left,jelly_rect.top,jelly_rect.width + score_rect.width + 6,jelly_rect.height)

		pygame.draw.rect(game,(167,209,61),bg_rect)
		game.blit(score_surface,score_rect)
		game.blit(jelly,jelly_rect)
		pygame.draw.rect(game,(56,74,12),bg_rect,2)

# parameters (can be set from outside)
cell_number = 10
cell_size=50
snake_length = 2
fruit_num = 0 # initial fruit numbers
dt=250 # tick delay (ms)
eat_rate = 0.25 # probability of eaten punishment (not instant dead on collision), bounded in (0,1) if out of bount, nothing happen. The more, the easier to grow, the harder to win.
static=True # if snake are allowed to be static
grass_color = (167,209,61)
low_grass = (175,215,70)
# dummy variable, need setup
scr=None # real screen
game=None # game draw surface
game_rect=None # game draw rect
main_game=None
# setup functions
def setup():
	global game,game_rect,scr
	pygame.init()
	scr=pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
	scr_rect=scr.get_rect()
	game=pygame.Surface((cell_size*cell_number,cell_size*cell_number))
	game_rect=game.get_rect(center=(scr_rect.centerx,scr_rect.centery))
# start screen
def main():
	global game,game_rect,scr,cell_size,main_game
	clock = pygame.time.Clock()

	main_game = MAIN()
	while True:
		if all(iden):
			main_game.update()
		main_game.draw_elements()
		scr.blit(game,game_rect)
		pygame.display.update()
		clock.tick(1000//dt)

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

iden=[False,False]

def handle_client(conn, addr): # May added to the users for them to host themselves
	global main_game,iden
	print(f"[NEW CONNECTION] {addr} connected.")
	identity=-1
	for i in range(len(iden)):
		if not iden[i]:
			identity=i
			break
	if identity<0:
		conn.close()
	iden[identity]=True

	connected = True
	while connected:
		msg = conn.recv(1).decode(FORMAT)
		if msg:
			if msg == 'q':
				connected = False
				iden[identity]=False
			if msg == 'd':
				main_game.snake[identity].direction = Vector2(0,-1)
			if msg == 'r':
				main_game.snake[identity].direction = Vector2(1,0)
			if msg == 'u':
				main_game.snake[identity].direction = Vector2(0,1)
			if msg == 'l':
				main_game.snake[identity].direction = Vector2(-1,0)
			if msg == 's':
				screen_data=pygame.image.tostring(scr,'RGB')
				buffer = str(len(screen_data)).encode(FORMAT)
				buffer += b' ' * (HEADER-len(buffer))
				conn.send(buffer)
				conn.send(screen_data)
	conn.close()

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__=='__main__':
	setup()
	threading.Thread(target=main).start()
	start()
	pygame.quit()