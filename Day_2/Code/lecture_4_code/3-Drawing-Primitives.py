import sys, pygame 
from pygame.locals import * 

pygame.init()

""" screen_rect = pygame.Rect(0,0,640,480)

Als erstes haben wir ein pygame.Rect hinzugefügt, 
das mit der pygame.Surface GAME_SCREEN verbunden ist, 
so dass wir uns leicht auf Stellen auf dem Screen 
beziehen können. 

Daher:
screen_rect.center bezieht sich auf die (x,y) Position 
des zentralen Pixels auf dem gesamten Screen.
"""
screen_rect = pygame.Rect(0,0,640,480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height))
pygame.display.set_caption('Drawing')


""" WHITE

Dann erstellen wir eine Variable WHITE, 
in der wir die rbg-Werte (rot, blau, grün) speichern,
die im Computer die Farbe Weiß ergeben.
"""
WHITE = (255, 255, 255) # rgb color values.

""" pygame.draw.circle - Was wir dem Computer sagen: 

- Zeichne einen Kreis auf der GAME_SCREEN Oberfläche
- Weiss machen
- Die Mitte sollte sich in der Mitte des Bildschirms befinden.
- Der Radius ist 20 Pixel
"""
pygame.draw.circle(GAME_SCREEN, WHITE, screen_rect.center, 20)

while True:
   for event in pygame.event.get():
       if event.type == QUIT:
           pygame.quit()
           sys.exit()
   pygame.display.update()