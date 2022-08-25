import pygame, random
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites

class Ghost(Entity):
    def __init__(self, node, pacmans=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacmans = pacmans
        self.total_dt = 0
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        self.total_dt += dt
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        allAlive = True
        for pac in self.pacmans:
            if not pac.alive:
                allAlive = False
        if allAlive:
            pac_index = int(self.total_dt / 10) % len(self.pacmans)
        elif self.pacmans[0].alive:
            pac_index = 0
        else:
            pac_index = 1
        self.goal = self.pacmans[pac_index].position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection         

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)




class Blinky(Ghost):
    def __init__(self, node, pacmans=None, blinky=None):
        Ghost.__init__(self, node, pacmans, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class GhostGroup(object):
    def __init__(self, node, pacmans):
        self.blinky = Blinky(node, pacmans)
        self.pinky = Pinky(node, pacmans)
        self.inky = Inky(node, pacmans, self.blinky)
        self.clyde = Clyde(node, pacmans)
        self.ghosts = [self.blinky]#, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

