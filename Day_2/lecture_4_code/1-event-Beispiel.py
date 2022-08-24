import pygame # import the pygame library
from pygame.locals import * # provides constant variables like QUIT
import sys # commonly used library in Python. We use it to end the program.

pygame.init() # needed for other pygame functions to work
pygame.display.set_mode((640, 480)) # sets up a window with 640x480 dimensions

while True: # main game loop
   for event in pygame.event.get(): # get events and iterate through them
       if event.type == QUIT: # if user clicks exit button
           pygame.quit() # Deactivates the pygame library
           sys.exit() # ends the whole program