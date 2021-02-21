# original code at https://github.com/clear-code-projects/Snake
# modified by Hanchai Nonprasart

import pygame,os
from ..server import client

# parameters (can be set from outside)
fps=30 # frame per second
# dummy variable, need setup
scr=None # real screen
game=None # game draw surface
game_rect=None # game draw rect
# setup functions
def setup():
	global game,game_rect,scr
	scr=pygame.display.get_surface()
	scr_rect=scr.get_rect()
	game=pygame.Surface((min(pygame.display.get_window_size()),min(pygame.display.get_window_size())))
	game_rect=game.get_rect(center=(scr_rect.centerx,scr_rect.centery))
	client.connect(os.getenv('IP'))
# start screen
def main():
	global game,game_rect,scr
	clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				scr=None
				game_rect=None
				game=None
				cell_size=None
				client.quit()
				return 0 # exit screen, need new setup, may include parameters needed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					client.move('d')
				if event.key == pygame.K_d:
					client.move('r')
				if event.key == pygame.K_s:
					client.move('u')
				if event.key == pygame.K_a:
					client.move('l')
		scr.blit(pygame.transform.smoothscale(pygame.image.fromstring(client.get(), (500,500), 'RGB'), game_rect.size), game_rect)
		pygame.display.update()
		clock.tick(fps)

if __name__=='__main__':
	pygame.init()
	pygame.display.set_mode((400,400))
	setup()
	main()
	pygame.quit()