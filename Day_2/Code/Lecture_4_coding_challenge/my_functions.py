""" 
Functions we write to help us keep our other code clean. 

You do not have to change anything in this file to solve the bugs.
"""
import pygame

def load_image(file_path, size=None, scale=None):
    """ 
    size: tuple (width, height)
    scale: integer value to scale the image
    """
    # file = os.path.join(file)
    surface = pygame.image.load(file_path)
    if size:
        surface = pygame.transform.scale(surface, size)
    if scale:
        rect = surface.get_rect()
        surface = pygame.transform.scale(surface, (scale*rect.width, scale*rect.height))
    return surface



class Lives(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.color = "white"
        self.lives = 3
        self.lastlives = 4
        self.update()
        self.rect = self.image.get_rect().move(10, 52)

    def update(self):
        """We only update the lives in update() when it has changed."""
        if self.lives != self.lastlives:
            self.lastlives = self.lives
            msg = "Lives: %d" % self.lives
            self.image = self.font.render(msg, 0, self.color)


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.color = "white"
        self.lastscore = -1
        self.score = 0
        self.update()
        self.rect = self.image.get_rect().move(10,10)

    def update(self):
        """We only update the score in update() when it has changed."""
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Score: %d" % self.score
            self.image = self.font.render(msg, 0, self.color)
        
class GameOver(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.color = "white"
        self.image = self.font.render("GAME OVER", 0, self.color)
        self.rect = self.image.get_rect(center=center)



class Background(pygame.sprite.Sprite): # extends sprite class
    def __init__(self, image):    
        super().__init__() # inherits init function from base class
        self.image = image
        self.rect = self.image.get_rect()

""" Authored by Allie Lahnala (alahnala@gmail.com) for the Hessian IT Summer School 2022 at University of Marburg"""

