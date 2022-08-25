import pygame, random, math
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from collections import defaultdict

class Pacman(Entity):
    def __init__(self, node, color, playerNum):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = color
        self.direction = LEFT
        self.alive = True
        self.lives = 3
        self.score = 0
        self.invincible = True
        self.invincibleTimer = 3
        self.playerNum = playerNum
        self.sprites = PacmanSprites(self, color)
        self.setBetweenNodes(LEFT)
        self.dt = defaultdict(lambda: 0)
        self.resets = defaultdict(lambda: False)
        if playerNum == 0:
            self.position.x += TILEWIDTH
        else:
            self.position.x -= TILEWIDTH

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.invincible = True
        self.invincibleTimer = 3
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def resetTimer(self, index):
        self.resets[index] = True

    def die(self):
        self.alive = False
        self.direction = STOP

    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                directions.append(key)
        # if len(directions) == 0:
        if self.direction * -1 not in directions:
            directions.append(self.direction * -1)
        return directions

    def update(self, dt, opponent, pellets, fruit, ghosts):
        for key in self.dt.keys():
            self.dt[key] += dt
        self.sprites.update(dt, self.invincibleTimer)
        self.position += self.directions[self.direction]*self.speed*dt

        if self.invincibleTimer > 0:
            self.invincibleTimer -= dt
        else:
            self.invincible = False

        if len(pellets.pelletList) > 0:
            pelletDists = []
            for pellet in pellets.pelletList:
                pelletDists.append(self.tileDistance(pellet))
            index = pelletDists.index(min(pelletDists))
            for i in range(len(pellets.pelletList)):
                if pellets.pelletList[i].color == self.color and i != index:
                    pellets.pelletList[i].color = WHITE
                elif i == index:
                    pellets.pelletList[i].color = self.color

        if self.alive:
            direction = self.move(opponent, pellets, fruit, ghosts)
            # if self.playerNum==0:
            #     print('move1: ' + DIRECTION_NAMES[direction])

            if self.overshotTarget():#debug=self.playerNum==0
                self.node = self.target
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
                direction = self.move(opponent, pellets, fruit, ghosts)
                # if self.playerNum==0:
                #     print('move2: ' + DIRECTION_NAMES[direction])
                self.target = self.getNewTarget(direction)
                if self.target is not self.node:
                    self.direction = direction
                    # print('self.direction = ' + DIRECTION_NAMES[self.direction])
                else:
                    # print('no new target')
                    self.target = self.getNewTarget(self.direction)

                if self.target is self.node:
                    self.direction = STOP
                self.setPosition()
            else:
                if self.oppositeDirection(direction):
                    self.reverseDirection()
        else:
            direction = STOP

        # if self.playerNum==0:
        #     print('now moving: ' + DIRECTION_NAMES[self.direction])

        for key in self.resets.keys():
            if self.resets[key]:
                self.resets[key] = False
                self.dt[key] = 0
                # print('resetting timer ' + str(key))

    def move(self, opponent, pellets, fruit, ghosts):
        return self.getValidKey()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    def render(self, screen):
        Entity.render(self, screen)
        # pygame.draw.circle(screen, RED, self.position.asInt(), 5)
        # pygame.draw.rect(screen, RED, Rect(self.position.x+TILEWIDTH/2, self.position.y+TILEWIDTH/2, TILEWIDTH/2, TILEHEIGHT/2), 2)
        # if self.node:
        #     self.node.render(screen)
