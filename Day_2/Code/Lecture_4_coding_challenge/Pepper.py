"""
Bug 1: Oh no! The pepper flies away!

Can you find a bug in the code that is making that happen?
"""
import random, pygame


class Pepper(pygame.sprite.Sprite):
    def __init__(self, image, start_position):    
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop=start_position)
        self.speed = 10 
 
    def update(self):
        self.rect.y = self.rect.y - self.speed

    def go_to_x(self, left, right):
        new_x_position = random.randint(left, right)
        self.rect.midtop = (new_x_position, 0)


""" Authored by Allie Lahnala (alahnala@gmail.com) for the Hessian IT Summer School 2022 at University of Marburg"""