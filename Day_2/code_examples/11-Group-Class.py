import sys, pygame 
from pygame.locals import * 

pygame.init() 
clock = pygame.time.Clock() 

screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Pepper Group Class') 


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

class PepperGroup:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def update(self):
        for item in self.items:
            item.update()
    
    def draw(self, surface):
        for item in self.items:
            item.draw(surface)

    def touch_ground_update(self, ground_rect):
        for item in self.items:
            if item.rect.bottom >= ground_rect.bottom:
                item.rect.top = ground_rect.top


pepper_list = PepperGroup()

pepper = Pepper(pygame.Rect(0, 0, 80, 100), screen_rect.midtop)
pepper2 = Pepper(pygame.Rect(0, 0, 40, 50), 
                (pepper.rect.left - 100, pepper.rect.top))

pepper_list.add(pepper)
pepper_list.add(pepper2)

while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()
    GAME_SCREEN.fill(WHITE)

    pepper_list.update()
    pepper_list.touch_ground_update(screen_rect)
    pepper_list.draw(GAME_SCREEN)

    pygame.display.update()
    clock.tick(10)


