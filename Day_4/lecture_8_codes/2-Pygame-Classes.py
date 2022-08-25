""" Imports, initialization, and constants """
import sys, pygame 
from pygame.locals import * 
import pathlib
code_dir = pathlib.Path(__file__).parent.resolve()

pygame.init() 
SCREEN_RECT = pygame.Rect(0,0,640, 480)
WHITE = (255, 255, 255) 
GAME_SCREEN = pygame.display.set_mode((SCREEN_RECT.width, SCREEN_RECT.height)) 
pygame.display.set_caption('Pygame Classes and Modules')

""" Player class """
class Player(pygame.sprite.Sprite):
    def __init__(self, image, midbottom, speed=10):    
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.speed = speed

    def move(self, keystates, boundaries):
        x_dir = keystates[K_RIGHT] - keystates[K_LEFT]
        y_dir = keystates[K_DOWN] - keystates[K_UP]
        self.rect = self.rect.move(x_dir * self.speed, y_dir * self.speed)
        self.rect.clamp_ip(boundaries)

""" Load image function """
def load_image(file_path, size=None, scale=None):
    """ 
    size: tuple (width, height)
    scale: integer value to scale the image
    """
    surface = pygame.image.load(file_path)
    if size:
        surface = pygame.transform.scale(surface, size)
    if scale:
        rect = surface.get_rect()
        surface = pygame.transform.scale(surface, (scale*rect.width, scale*rect.height))
    return surface

""" Main function """
def main():

    img = load_image("imgs/kitty.png", scale=3)
    player = Player(img, SCREEN_RECT.midbottom)
    sprites = pygame.sprite.Group()
    sprites.add(player) 
    clock = pygame.time.Clock()
    while True: 
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                pygame.quit() 
                sys.exit()
        GAME_SCREEN.fill(WHITE)        
        keystates = pygame.key.get_pressed()
        player.move(keystates, SCREEN_RECT)
        sprites.draw(GAME_SCREEN)
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
