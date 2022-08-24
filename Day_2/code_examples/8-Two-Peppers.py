import sys, pygame 
from pygame.locals import * 

pygame.init() 
clock = pygame.time.Clock() 

screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Pepper Class Methods') 


WHITE = (255, 255, 255) 
RED = (255, 0, 0) 

class Pepper:
    speed = 20
    color = RED
    
    def __init__(self, rect, midtop):
        self.rect = rect
        self.rect.midtop = midtop
    
    def update(self):
        self.rect.top = self.rect.top + self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


pepper = Pepper(pygame.Rect(0, 0, 80, 100), screen_rect.midtop)
pepper2 = Pepper(pygame.Rect(0, 0, 40, 50), 
                (pepper.rect.left - 100, pepper.rect.top))
while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()
    GAME_SCREEN.fill(WHITE)
    pepper.update()
    pepper2.update()
    pepper.draw(GAME_SCREEN)
    pepper2.draw(GAME_SCREEN)
    pygame.display.update()
    clock.tick(1)


