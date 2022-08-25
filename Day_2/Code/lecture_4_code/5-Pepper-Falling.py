"""
Wir wollen ein rotes Rechteck vom oberen Rand des Bildschirms fallen lassen.

Was sind die Komponenten unserer Spielschleife?

Handle events: Betrachte den Ablauf der Zeit als ein Ereignis
Update game state: Die y-Position des Rechtecks soll sich erhöhen
Draw: Zeichne das Rechteck an seiner richtigen Position
"""
import sys, pygame
from pygame.locals import *

pygame.init()
""" 1. clock = pygame.time.Clock()
Wir haben eine Uhr hinzugefügt, 
mit der wir steuern können, 
wie schnell die Spielschleife iteriert.
"""
clock = pygame.time.Clock()

screen_rect = pygame.Rect(0,0,640, 480)
GAME_SCREEN = pygame.display.set_mode((screen_rect.width, screen_rect.height)) 
pygame.display.set_caption('Drawing in the loop')
RED = (255, 0, 0) 

""" 3. Das rechteckige Objekt
Stellen wir uns dieses rechteckige Objekt als Pepper vor :)
Vor der Game Loop müssen wir einige Eigenschaften der Pepper definieren.
"""
pepper_width = 80
pepper_height = 100
pepper_rect = pygame.Rect(0, 0, pepper_width, pepper_height)
pepper_rect.centerx = screen_rect.centerx
pepper_rect.top = screen_rect.top
pepper_color = RED
pepper_speed = 20


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    """ 6. 
    Unser Code zeichnet Rechtecke, 
    aber die vorherige Zeichnung bleibt auf dem Screen!
    Was können wir tun?
    """
    # your code here (see slides)

    """ 5. Die Position updaten 
    Damit die Pepper fällt, müssen wir die Position updaten. 
    Hinzufügen zum update code.
    """
    # your code here (see slides)


    """ 4. Zeichne das Rechteck an seiner richtigen Position
    Wir fügen den drawing part in die game loop direkt vor 
        pygame.display.update() ein
    """
    pygame.draw.rect(GAME_SCREEN, pepper_color, pepper_rect)
    pygame.display.update()
    """ 2. clock.tick(1)
    Eine Iteration ist ein Frame. Wenn wir also clock.tick(1) aufrufen, 
    sagen wir, dass die Geschwindigkeit ein Frame pro Sekunde (FPS) sein soll
    """
    clock.tick(1)
