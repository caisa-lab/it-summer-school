from ball import Ball
from constants import *


class Paddle:
    COLOR = WHITE
    VEL = 4
    INIT_VEL = 4
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y 
        self.width = width
        self.height = height
        self.hits = 0
        self.ai = False
        
        
    def predict(self, ball: Ball):
        pass
            
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))    

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL                 
                
    def increase_vel(self):
        self.VEL += 1
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.VEL = self.INIT_VEL
    
    
class AiPaddle(Paddle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.ai = True
        
        self.pred_x = self.original_x
        self.pred_y = self.original_y
        self.random_slide = 0
        self.move_up = None
    
    def predict(self, ball: Ball):
        """
        TODO: Implement the function predict()
        Hint: The paddle needs to go where the ball goes
        """
            
    def move(self, up=True):
        if up:
            if self.y - self.VEL < self.pred_y:
                self.y = self.pred_y
            else:
                self.y -= self.VEL
        else:
            if self.y + self.VEL > self.pred_y:
                self.y = self.pred_y
            else:
                self.y += self.VEL
                
    def reset(self):
        super().reset()
        self.pred_x = self.original_x
        self.pred_y = self.original_y
        self.move_up = not self.move_up