
import pygame, random, math
from pygame.locals import *
from pacman import Pacman
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from collections import defaultdict

class MyPacmanAI1(Pacman):
    def __init__(self, node, playerNum):
        color = TEAL
        Pacman.__init__(self, node, color, playerNum)

    def move(self, opponent, pellets, fruit, ghosts):
        directions = self.validDirections()
        self.goal = ghosts.blinky.position
        printDirections(directions)
        directions = self.goalDirection(directions)
        direction = random.choice(directions)
        return direction

class MyPacmanAI2(Pacman):
    def __init__(self, node, playerNum):
        color = ORANGE
        Pacman.__init__(self, node, color, playerNum)

    def move(self, opponent, pellets, fruit, ghosts):
        return self.direction
