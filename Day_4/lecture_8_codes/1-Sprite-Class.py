import sys, pygame 
from pygame.locals import * 

pygame.init() 
clock = pygame.time.Clock() 

screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Sprite Class') 

WHITE = (255, 255, 255) 
RED = (255, 0, 0) 
BLUE = (0, 0, 255) 


class Sprite:
    def __init__(self, rect, color):
        print("Sprite.__init__")
        self.rect = rect
        self.color = color
    
    def update(self):
        print("Sprite.update")
        """ 
        Our sprites are updated in different ways, 
        so we can leave this unimplemented
        """
        return

    def draw(self, surface):
        print("Sprite.draw")
        """ 
        In our game, the sprites are drawn the same.
        """
        pygame.draw.rect(surface, self.color, self.rect)


class Pepper(Sprite):
    def __init__(self, rect, color=RED, speed=10):
        super().__init__(rect, color)
        print("Pepper.__init__")
        self.speed = speed
    
    def update(self):
        print("Pepper.update")
        self.rect.top = self.rect.top + self.speed

    def touch_ground_update(self, ground_rect):
        print("Pepper.touch_ground_update")
        if self.rect.bottom >= ground_rect.bottom:
            self.rect.top = ground_rect.top


class Player(Sprite):
    def __init__(self, rect, color=BLUE, speed=10):
        super().__init__(rect, color)
        print("Player.__init__")
        self.speed = speed
    
    def move(self, keystates):
        print("Player.move")
        if keystates[K_LEFT] or keystates[K_a]:
            self.rect.x = self.rect.x - self.speed
        if keystates[K_RIGHT] or keystates[K_d]:
            self.rect.x = self.rect.x + self.speed

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



pepper = Pepper(pygame.Rect(0, 0, 80, 100))
pepper.rect.midtop = screen_rect.midtop

player = Player(pygame.Rect(0, 0, 80, 80))
player.rect.midbottom = screen_rect.midbottom

while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()
    GAME_SCREEN.fill(WHITE)
    pepper.update()
    keystates = pygame.key.get_pressed()
    player.move(keystates)
    pepper.touch_ground_update(screen_rect)
    pepper.draw(GAME_SCREEN)
    player.draw(GAME_SCREEN)
    pygame.display.update()
    clock.tick(1)
    quit()
