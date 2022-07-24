import sys
import pygame
from settings import Settings

class AlienInvasion:

    def __init__(self):

        settings=Settings()
        self.screen=pygame.display.set_mode(size=(settings.screen_width,settings.screen_heigth),flags=(pygame.RESIZABLE))
        pygame.display.set_caption('Alien_Invasion')

        self.bg_color=(settings.bg_color)



        

    def run_game(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            
            self.screen.fill(self.bg_color)
            pygame.display.flip()

if __name__=='__main__':
    ai = AlienInvasion()
    ai.run_game()
            