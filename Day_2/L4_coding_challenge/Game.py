"""
Bug 3: Oh no! The pepper always goes to the center of the screen once the cat catches it!

Help us find the code that causes this to happen!
"""

import pygame, sys
from pygame.locals import *
import my_functions
from Player import Player
from Pepper import Pepper
from my_functions import Score, Lives, GameOver, Background
import pathlib
code_dir = str(pathlib.Path(__file__).parent.resolve()) # used to know the location of image files

pygame.init()
pygame.display.set_caption('Cat wants peppers!')
icon = my_functions.load_image(code_dir + "/images/kitty.png", size=(32,32))
pygame.display.set_icon(icon)
SCREENRECT = pygame.Rect(0, 0, 640, 480)


def main():

    screen = pygame.display.set_mode(SCREENRECT.size)
    sprites = pygame.sprite.Group()

    """ setup background """
    img = my_functions.load_image(code_dir + "/images/backdrop.png", size=SCREENRECT.size)
    background = Background(img)
    sprites.add(background)

    """ make player object """
    img = my_functions.load_image(code_dir + "/images/kitty.png", scale=3)
    player = Player(img, SCREENRECT.midbottom)
    sprites.add(player) 

    """ make pepper object """
    img = my_functions.load_image(code_dir + "/images/pepper.png", scale=3)
    pepper = Pepper(img, SCREENRECT.midtop)
    sprites.add(pepper)

    """ make score object """
    score_display = Score()
    sprites.add(score_display)

    """ make lives object """
    lives_display = Lives()
    sprites.add(lives_display)


    clock = pygame.time.Clock()
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

      
        sprites.update()

        keystate = pygame.key.get_pressed()
        player.move(keystate)
        player.rect.clamp_ip(SCREENRECT) # handles the player not going out of bounds


        if pygame.sprite.collide_rect(pepper, player):
            pepper.go_to_x(SCREENRECT.centerx, SCREENRECT.centerx)
            score_display.score = score_display.score + 1
            
        if pepper.rect.bottom > SCREENRECT.bottom:
            pepper.go_to_x(SCREENRECT.left, SCREENRECT.right)
            lives_display.lives = lives_display.lives - 1


        if lives_display.lives == 0:
            sprites.remove(player)
            sprites.remove(pepper)
            sprites.add(GameOver(SCREENRECT.center))


        sprites.draw(screen)
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()


""" Authored by Allie Lahnala (alahnala@gmail.com) for the Hessian IT Summer School 2022 at University of Marburg"""