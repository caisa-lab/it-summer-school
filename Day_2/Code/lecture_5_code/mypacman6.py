
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
        d2ghost = self.tileDistance(ghosts.blinky)
        scores = {UP: 0, DOWN: 0, RIGHT: 0, LEFT: 0}

        if d2ghost < 10:
            self.goal = ghosts.blinky.position
            directions = self.validDirections()
            if ghosts.blinky.mode.current == FREIGHT:
                directions = self.goalDirection(directions)
                for d in directions:
                    scores[d] += 20
            else:
                directions = self.goalDirection(directions, minimize=False)
                for d in directions:
                    scores[d] += 10

        if len(pellets.pelletList) > 0:
            pelletDists = []
            for pellet in pellets.pelletList:
                pelletDists.append(self.tileDistance(pellet))
            mindist = min(pelletDists)
            index = pelletDists.index(mindist)
            self.goal = pellets.pelletList[index].position
            directions = self.validDirections()
            directions = self.goalDirection(directions)
            for d in directions:
                scores[d] += 5

        direction = max(scores, key=scores.get)
        return direction

class MyPacmanAI2(Pacman):
    def __init__(self, node, playerNum):
        color = ORANGE
        Pacman.__init__(self, node, color, playerNum)

    def move(self, opponent, pellets, fruit, ghosts):
        return self.direction
