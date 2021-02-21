# Hanchai Nonprasart
import pygame

from . import gameplay,start

def main():
	pygame.init()
	start.setup() # set initial screen
	while True:
		screenID=0
		if screenID<0: # exit screen
			pygame.quit() # close program
			return 0 # quit successfully
		if screenID==0:
			screenID=start.main() # start initial screen
		if screenID==1:
			gameplay.setup() # set screen to gameplay screen
			screenID=gameplay.main() # start gameplay screen
		raise(Exception('Index Error, screenID not in range'))
if __name__=='__main__':
	main()