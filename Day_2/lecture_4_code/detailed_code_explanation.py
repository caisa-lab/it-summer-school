import pygame, sys, random
from pygame.locals import * 


pygame.init()
pygame.display.set_caption('Time-update demo')

SCREENRECT = pygame.Rect(0, 0, 640, 480)
BLACK = (0, 0, 0)

""" here we make a function to load images, which we use right after to load the icon """
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

icon = load_image("images/pepper.png", size=(32,32))
pygame.display.set_icon(icon)



class Pepper(pygame.sprite.Sprite):
    def __init__(self, image, start_position):    
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop=start_position)
        self.speed = 10 
 
    def update(self):
        self.rect.y = self.rect.y + self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def go_to_x(self, left, right):
        new_x_position = random.randint(left, right)
        self.rect.midtop = (new_x_position, 0)


def main():

    """ Here we create our display surface where we draw our game. """
    screen = pygame.display.set_mode(SCREENRECT.size)

    """ make pepper object """
    img = load_image("images/pepper.png", scale=3)
    pepper = Pepper(img, SCREENRECT.midtop)


    """ Here we create a pygame.time.Clock object. 
    - We use the clock to help control the speed of the iterations.
    - The very last line of the while-loop shows calls clock.tick().
    - See that line of code for further explanation.
    """
    clock = pygame.time.Clock()

    """ Now our game loop begins. """
    while True:
        screen.fill(BLACK)
        """ First we get any events that pygame can give us. """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        """ Update sprites (time-based)
        - The pepper constantly updates its position based on the passage of time.
        - We implemented a method of the Pepper class Pepper.update() which handles that movement.
        - We call the update function in every iteration of game loop
        """
        pepper.update()



        """ Update peppers upon condition
        - Now, peppers do not only update because of time. They also update if they touch the 
            player or the ground.
        """
        if pepper.rect.bottom > SCREENRECT.bottom:
            pepper.go_to_x(SCREENRECT.left, SCREENRECT.right)


        """ Drawing the screen
        - Here, we call sprites.draw(screen). This draws the current state of all sprites in
            the sprite group `sprites` on the screen. That includes the background, player, and 
            pepper.
        """
        pepper.draw(screen)
        

        
        """ Update Display
        - pygame.display.update() is really important. Though we have drawn the sprites onto 
            `screen,` screen is just a pygame.Surface object. To update part of our game window
            where our game content should show (as opposed to the window border, title bar, and 
            exit & minimize buttons), we need to call this function.
        """
        pygame.display.update()

        """ Control the iteration speed with clock.tick(FPS)
        - The value passed into clock.tick() is the number of Frames per Second (FPS).
        - One frame is one iteration of the while-loop.
        - If FPS = 10, then the while-loop will iterate 10 times in one second.
        - When FPS = 1, the pepper falls 10 pixels (because pepper.speed = 10) per second.
            Likewise, the player can move up to 10 pixels per second. That is pretty slow!
        - Try different values for FPS and run the game to see its effect.
        """
        clock.tick(1)



if __name__ == "__main__":
    main()


""" Authored by Allie Lahnala (alahnala@gmail.com) for the Hessian IT Summer School 2022 at University of Marburg"""