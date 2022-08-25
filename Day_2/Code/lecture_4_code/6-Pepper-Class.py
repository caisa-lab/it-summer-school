import sys, pygame 
from pygame.locals import * 

pygame.init() 
clock = pygame.time.Clock() # control have fast to iterate

screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Pepper Class') 


WHITE = (255, 255, 255) 
RED = (255, 0, 0) 

class Pepper:
    speed = 20
    color = RED
    
    def __init__(self, rect, midtop):
        self.rect = rect
        self.rect.midtop = midtop


pepper = Pepper(pygame.Rect(0, 0, 80, 100), screen_rect.midtop)

while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()
    GAME_SCREEN.fill(WHITE)
    """ Update pepper to make it fall. """
    pepper.rect.top = pepper.rect.top + pepper.speed
    """ Draw pepper """
    pygame.draw.rect(GAME_SCREEN, pepper.color, pepper.rect)
    pygame.display.update()
    clock.tick(1)


