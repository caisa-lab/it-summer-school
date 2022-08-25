from constants import *


class Ball:
    INIT_VEL = 5
    MAX_VEL = 40
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y 
        self.radius = radius
        self.x_vel = self.INIT_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def increase_vel(self):
        if self.x_vel <= self.MAX_VEL:
            if self.x_vel < 0:
                self.x_vel -= 1
            else:
                self.x_vel += 1    
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel = self.INIT_VEL = -1 * self.INIT_VEL # reverse the direction
        