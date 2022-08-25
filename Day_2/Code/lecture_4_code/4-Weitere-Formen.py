import sys, pygame 
from pygame.locals import * 

pygame.init() 
screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Einfache Objekte zeichnen: Weitere Formen') 


""" More Colors """
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 

GAME_SCREEN.fill(WHITE)

"""
Viele weitere Formen können mit pygame.draw gezeichnet
werden, wie z.B. rect (rectangle), ellipse, arc, polygon.
"""
pygame.draw.circle(GAME_SCREEN, BLACK, screen_rect.center, 20)
pygame.draw.rect(GAME_SCREEN, RED, (screen_rect.left + 40, screen_rect.top, 30, 50))

my_rect = pygame.Rect(screen_rect.centerx, # top left x
                      screen_rect.centery + 20, # top left y
                      screen_rect.width / 8, # width of my_rect
                      screen_rect.height / 8) # height of my_rect
pygame.draw.rect(GAME_SCREEN, BLUE, my_rect)


while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit() 
    pygame.display.update()



