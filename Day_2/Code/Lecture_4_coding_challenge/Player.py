""" 
Bug 2: Oh no! We can't move the Player! 

We need your help making the player move.
Help us fix this by completing the `move` function below.
"""

import pygame
from pygame.locals import *



class Player(pygame.sprite.Sprite):
    def __init__(self, image, midbottom):    
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.speed = 10


    def move(self, keystate):
        left_arrow_pressed = keystate[K_LEFT]
        right_arrow_pressed = keystate[K_RIGHT]

        """ TODO: help us move the player!
        Write some code to move the player 
            left when the left arrow is pressed 
            and right when the right arrow is pressed.
        
        The two variables given in the function are
            Booleans, indicating whether or not the 
            left and right arrow keys are pressed
        """


        return

""" Authored by Allie Lahnala (alahnala@gmail.com) for the Hessian IT Summer School 2022 at University of Marburg"""