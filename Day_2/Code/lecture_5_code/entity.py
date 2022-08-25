import pygame, random
from pygame.locals import *
from vector import Vector2
from constants import *

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0, -1), DOWN:Vector2(0, 1),
                           LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if isinstance(direction, list):
                direction = random.choice(direction)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self, debug=False):
        returnValue = False
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            returnValue = node2Self >= node2Target
        if debug:
            print('overshot target: ' + str(returnValue))
        return returnValue

    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def validDirection(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[random.randint(0, len(directions)-1)]

    def goalDirection(self, directions, minimize=True):
        distances = []
        for direction in directions:
            goalDist = self.tileDistance(self.position + self.directions[direction]*TILEWIDTH, self.goal)
            distances.append(goalDist)

        matchValue = min(distances) if minimize else max(distances)
        indices = [i for i in range(len(directions)) if distances[i] == matchValue]
        goalDirections = []
        for i in range(len(directions)):
            if distances[i] == matchValue:
                goalDirections.append(directions[i])
        return goalDirections

    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        # self.speed = 100
        self.setSpeed(100)
        self.visible = True

    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

    def tileDistance(self, other, obj2=None):
        tp1 = other.position if not isinstance(other, Vector2) else other
        tp2 = self.position if not obj2 else (obj2.position if not isinstance(obj2, Vector2) else obj2)
        xdist = abs((tp2.x - tp1.x) / TILEWIDTH)
        ydist = abs((tp2.y - tp1.y) / TILEHEIGHT)
        return xdist + ydist
