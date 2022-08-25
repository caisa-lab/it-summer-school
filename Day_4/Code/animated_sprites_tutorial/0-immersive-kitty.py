""" Load a sprite sheet for the player and update the sprite image every loop iteration """
import pygame, sys
from pygame.locals import *
import utils
import pathlib
code_dir = str(pathlib.Path(__file__).parent.resolve()) # used to know the location of image files

pygame.init()
pygame.display.set_caption('Sprite sheets')
icon = utils.load_image(code_dir + "/imgs/kitty.png", size=(32,32))
pygame.display.set_icon(icon)
SCREENRECT = pygame.Rect(0, 0, 640, 480)
WHITE = (225,225,225)


def load_spritesheet(file_path, cols=1, scale=None, size=None):
    surface = utils.load_image(file_path, scale=scale, size=size)
    sheet_rect = surface.get_rect()
    image_width = int(sheet_rect.width / cols)

    images = []
    for i in range(0, sheet_rect.width, image_width):
        rect = pygame.Rect(i, 0, image_width, sheet_rect.height)
        image = surface.subsurface(rect)
        images.append(image)
    return images

class Player(pygame.sprite.Sprite):
    speed = 10
    def __init__(self, sprite_sheet) -> None:
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.current_image = 0
        self.image = self.sprite_sheet[self.current_image]
        self.rect = self.image.get_rect()

    def update(self):
        # short hand for if..else that assigns one variable
        self.current_image = 1 if self.current_image == 0 else 0
        self.image = self.sprite_sheet[self.current_image]

    def move(self, keystates, boundary):
        dx = self.speed * (keystates[K_RIGHT] - keystates[K_LEFT])
        self.rect.move_ip(dx, 0)
        self.rect.clamp_ip(boundary) 


def main():
    game_screen = pygame.display.set_mode(SCREENRECT.size)
    sprites = pygame.sprite.Group()

    """ make player object """
    player_sprites = load_spritesheet(code_dir + "/imgs/kitty-spritesheet.png", cols=2, scale=4)
    player = Player(player_sprites)
    player.rect.midbottom = SCREENRECT.midbottom
    sprites.add(player)

    FPS = 2
    clock = pygame.time.Clock()
    dt = 0
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        game_screen.fill(WHITE)        
        sprites.update()

        keystates = pygame.key.get_pressed()
        player.move(keystates, SCREENRECT)
        
        sprites.draw(game_screen)
        pygame.display.update()
        
        """
        - clock.tick(FPS) returns milliseconds since last tick
        - to get seconds, we can divide by 1000
        """
        dt = clock.tick(FPS) / 1000
        print(dt)

if __name__ == "__main__":
    main()