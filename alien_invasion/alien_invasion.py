import sys
import pygame

class AlienInvasion:

    def __init__(self):
        self.screec=pygame.display.set_mode(size=(1200,800),flags=(pygame.OPENGL))
        pygame.display.set_caption('AlienInvasion')

    def run_game(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            pygame.display.flip()

if __name__=='__main__':
    ai = AlienInvasion()
    ai.run_game()
            