import sys, pygame 
from pygame.locals import * 

pygame.init() 
clock = pygame.time.Clock() 

screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Add Player Rect') 


WHITE = (255, 255, 255) 
RED = (255, 0, 0) 
BLUE = (0, 0, 255) 


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
pepper_list.add(Pepper(pygame.Rect(0, 0, 80, 100), screen_rect.midtop))
pepper_list.add(Pepper(pygame.Rect(0, 0, 40, 50), 
                (pepper_list.items[0].rect.left - 100, pepper_list.items[0].rect.top)))


class Player:
    speed = 10
    color = BLUE
    
    def __init__(self, rect, midbottom):
        self.rect = rect
        self.rect.midbottom = midbottom
    
    def update(self):
        return

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

player = Player(pygame.Rect(0, 0, 80, 80), screen_rect.midbottom)
while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()
    GAME_SCREEN.fill(WHITE)

    pepper_list.update()
    player.update()
    pepper_list.touch_ground_update(screen_rect)
    pepper_list.draw(GAME_SCREEN)
    player.draw(GAME_SCREEN)
    pygame.display.update()
    clock.tick(10)


