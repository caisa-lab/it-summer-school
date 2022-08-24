""" Example from Slide 'Basic Game Loop in Pygame' """

import sys, pygame # import the pygame library
from pygame.locals import * # provides constant variables like QUIT

pygame.init() # needed for other pygame functions to work

""" Draw Screen: 
- Der Screen ist leer. 
- Wenn wir wollen, dass etwas erscheint, 
  müssen wir es auf die GAME_SCREEN-Oberfläche zeichnen.
"""
GAME_SCREEN = pygame.display.set_mode((640, 480)) # dimensions of display
pygame.display.set_caption('Basic game loop') # Adds title to window

while True: # Game loop
   for event in pygame.event.get(): # get events and iterate through them
       if event.type == QUIT: # if user clicks exit button
           pygame.quit() # Deactivates the pygame library
           sys.exit() # ends the whole program
   pygame.display.update()
