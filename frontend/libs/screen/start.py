
import pygame
fps=30
screen=None
def setup():
	global screen
	screen=pygame.display.set_mode((400,300))
	pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load('Graphics/cover.jpg').convert_alpha(), (25,25)))
	pygame.display.set_caption('MySlither.Academy')
def main():
	global screen
	clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				screen=None
				return -1
			if event.type == pygame.KEYDOWN:
				return 1
		screen.blit(pygame.transform.smoothscale(pygame.image.load('Graphics/cover.jpg').convert_alpha(), (400,300)),screen.get_rect())
		pygame.display.update()
		clock.tick(fps)
if __name__=='__main__':
	setup()
	main()