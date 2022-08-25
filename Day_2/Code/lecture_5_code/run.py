import pygame
from pygame.locals import *
from constants import *
from mypacman6 import MyPacmanAI1, MyPacmanAI2
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData

# PLAYER1_COLOR = TEAL#PINK
# PLAYER2_COLOR = ORANGE#GREEN

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.textgroup = TextGroup()
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman1 = MyPacmanAI1(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart), 0)
        self.pacman2 = MyPacmanAI2(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart), 1)
        self.pacmans = [self.pacman1, self.pacman2]
        self.lifesprites1 = LifeSprites(self.pacman1.lives)
        self.lifesprites2 = LifeSprites(self.pacman2.lives)
        self.lifesprites = [self.lifesprites1, self.lifesprites2]
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), [self.pacman1, self.pacman2])

#        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
#        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
#        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman1)
        self.nodes.denyHomeAccess(self.pacman2)
        self.nodes.denyHomeAccessList(self.ghosts)
#        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
#        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if not self.pacman1.alive or not self.pause.paused:
            self.pacman1.update(dt, self.pacman2, self.pellets, self.fruit, self.ghosts)
        if not self.pacman2.alive or not self.pause.paused:
            self.pacman2.update(dt, self.pacman1, self.pellets, self.fruit, self.ghosts)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman1.alive or self.pacman2.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            #self.hideEntities()

    def checkPelletEvents(self):
        for i in range(len(self.pacmans)):
            pellet = self.pacmans[i].eatPellets(self.pellets.pelletList)
            if pellet:
                self.pellets.numEaten += 1
                self.updateScore(pellet.points, i)
                if self.pellets.numEaten == 30:
                    self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
                if self.pellets.numEaten == 70:
                    self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
                self.pellets.pelletList.remove(pellet)
                if pellet.name == POWERPELLET:
                    self.ghosts.startFreight()
                if self.pellets.isEmpty():
                    self.flashBG = True
                    # self.hideEntities()
                    # self.pause.setPause(pauseTime=3, func=self.nextLevel)
                    self.textgroup.showText(GAMEOVERTXT)
                    print("Player 1 Score: " + str(self.pacmans[0].score))
                    print("Player 2 Score: " + str(self.pacmans[1].score))
                    self.pause.setPause(pauseTime=60, func=self.restartGame)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            for i in range(len(self.pacmans)):
                if self.pacmans[i].collideGhost(ghost):
                    if ghost.mode.current is FREIGHT:
                        if self.pacmans[i].alive:
                            self.pacmans[i].visible = False
                            ghost.visible = False
                            self.updateScore(ghost.points, i)
                            self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, FONT_SIZE, time=1)
                            self.ghosts.updatePoints()
                            self.pause.setPause(pauseTime=1, func=self.showEntities)
                            ghost.startSpawn()
                            self.nodes.allowHomeAccess(ghost)
                    elif ghost.mode.current is not SPAWN:
                        if self.pacmans[i].alive and not self.pacmans[i].invincible:
                            self.pacmans[i].lives -=  1
                            self.lifesprites[i].removeImage()
                            self.pacmans[i].die()
                            # self.ghosts.hide()
                            if self.pacmans[0].lives <= 0 and self.pacmans[1].lives <=0:
                                self.textgroup.showText(GAMEOVERTXT)
                                print("Player 1 Score: " + str(self.pacmans[0].score))
                                print("Player 2 Score: " + str(self.pacmans[1].score))
                                self.pause.setPause(pauseTime=60, func=self.restartGame)
                            if self.pacmans[i].lives > 0:
                                self.pacmans[i].reset()
                            # else:
                            #     self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)
        for i in range(len(self.pacmans)):
            if self.fruit is not None:
                if self.pacmans[i].collideCheck(self.fruit):
                    self.updateScore(self.fruit.points, i)
                    self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, FONT_SIZE, time=1)
                    fruitCaptured = False
                    for fruit in self.fruitCaptured:
                        if fruit.get_offset() == self.fruit.image.get_offset():
                            fruitCaptured = True
                            break
                    if not fruitCaptured:
                        self.fruitCaptured.append(self.fruit.image)
                    self.fruit = None
                elif self.fruit.destroy:
                    self.fruit = None

    def showEntities(self):
        self.pacman1.visible = True
        self.pacman2.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman1.visible = False
        self.pacman2.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.pacmans[0].lives = 3
        self.pacmans[1].lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        for i in range(len(self.pacmans)):
            self.pacmans[i].score = 0
            self.textgroup.updateScore(self.pacmans[i].score, i)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites1.resetLives(self.pacmans[0].lives)
        self.lifesprites2.resetLives(self.pacmans[1].lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = True
        self.pacman1.reset()
        self.pacman2.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def updateScore(self, points, index):
        self.pacmans[index].score += points
        self.textgroup.updateScore(self.pacmans[index].score, index)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        # self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman1.render(self.screen)
        self.pacman2.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites1.images)):
            x = self.lifesprites1.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites1.images[i].get_height()
            colorImage = pygame.Surface(self.lifesprites1.images[i].get_size()).convert_alpha()
            colorImage.fill(self.pacman1.color)
            ss_image = self.lifesprites1.images[i].copy()
            ss_image.blit(colorImage, (0,0), special_flags=pygame.BLEND_MULT)
            self.screen.blit(ss_image, (x, y))

        for i in range(len(self.lifesprites2.images)):
            x = SCREENWIDTH - self.lifesprites2.images[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.lifesprites2.images[i].get_height()
            colorImage = pygame.Surface(self.lifesprites2.images[i].get_size()).convert_alpha()
            colorImage.fill(self.pacman2.color)
            ss_image = self.lifesprites2.images[i].copy()
            ss_image.blit(colorImage, (0,0), special_flags=pygame.BLEND_MULT)
            self.screen.blit(ss_image, (x, y))

        # for i in range(len(self.fruitCaptured)):
        #     x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
        #     y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
        #     self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()



