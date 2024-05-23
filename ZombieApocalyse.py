import pygame
from sys import exit
from pygame.locals import *
import random
import math
from gameDB import *

class Player():
    def __init__(self, name, color, positions, x = 100, y = 100):
        self.x = x
        self.y = y
        self.name = name
        self.radius = 15
        self.score = 0
        self.color = color
        self.numKills = 0
        self.numShots = 0
        self.angle = 0
        self.speed_x = 2
        self.speed_y = 2
        self.gun_range = 20
        self.counter = 0
        self.reload = 60
        self.health = 1000
        self.positions = positions

    def isDead(self):
        if self.health == 0:
            return True
    
    def rotateGunLeft(self):
        self.angle -= math.pi/90
    
    def rotateGunRight(self):
        self.angle += math.pi/90
    
    def moveLeft(self):
        self.x -= 4
        if self.x < 15:
            self.x = 15

    def moveRight(self):
        self.x += 4
        if self.x > 1185:
            self.x = 1185

    def moveUp(self):
        self.y -= 4
        if self.y < 65:
            self.y = 65

    def moveDown(self):
        self.y += 4
        if self.y > 585:
            self.y = 585

    def hit(self):
        self.color = red
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x + self.gun_range*math.cos(self.angle), self.y + self.gun_range*math.sin(self.angle)) , 2)
        
    def renderInfo(self):
        health_percentage = self.health/1000
        new_x = 300*health_percentage
        screen.blit(font.render(self.name, True, (255, 255, 255)), self.positions[0])
        screen.blit(font.render(str(round(self.score, 0)), True, red), self.positions[1])
        pygame.draw.line(screen, red,  self.positions[2], (self.positions[3]+new_x, 40), 10)
        if self.health != 1000:
            pygame.draw.line(screen, white, (self.positions[3]+new_x, 40), (self.positions[3]+300, 40), 10)

            
class Bullet:
    def __init__(self, x, y, radius, angle, player, color, speed):
        self.x = x
        self.y = y
        self.d = 10
        self.speed = speed
        self.angle = angle
        self.color = orange
        self.player = player

    def draw(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.d, self.d))
        
    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def hit(self):
        if (self.x <= 0 or self.x >= 1200) or (self.y <= 60 or self.y >= 600):
            return True
        else:
            return False
        
        
class Zombie():
    def __init__(self, x, y, speed, health):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = green
        self.speed = speed
        self.health = health

    def determineDirection(self):
        if my_player.isDead():
            dst1 = 1000000000000000000000000000000000000000
        else:
           dst1 = distance(self.x, self.y, my_player.x, my_player.y)
        if player_two.isDead():
            dst2 = 1000000000000000000000000000000000000000
        else:
            dst2 = distance(self.x, self.y, player_two.x, player_two.y)
        if  dst1 < dst2:
            calcY = self.y - my_player.y
            calcX = self.x - my_player.x
        else:
            calcY = self.y - player_two.y
            calcX = self.x - player_two.x
        if calcX == 0:
            calcX = 0.00000000000000000001
        if calcX < 0:
            direction = math.atan(calcY / calcX)
        else:
            direction = math.atan(calcY / calcX) + math.pi
        if dst1 < 400 or dst2 < 400:
            return direction
        else:
            return direction + (random.randint(0, 180) - 90) * math.pi/360

    def damages(self, my_player):
        if distance(self.x, self.y, my_player.x, my_player.y) < 25:
            my_player.hit()
            my_player.health -= 1
            
    def move(self):
        dire = self.determineDirection()
        self.x += self.speed * math.cos(dire)
        self.y += self.speed * math.sin(dire)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
class Mouse(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def print(self):
        return str(self.x) + " ," + str(self.y)
class HomeIcon:
    def __init__(self):
        self.block = (900, 500, 50, 30)
        self.roof = [(890, 500), (960, 500), (925, 470)]
        self.door = (920, 509, 10, 21)
        self.color = white
    def draw(self):
        pygame.draw.rect(screen, self.color, self.block)
        pygame.draw.polygon(screen, self.color, self.roof)
        pygame.draw.rect(screen, blue, self.door)
    
pygame.init()

screen = pygame.display.set_mode((1200, 600), 0, 32)
cover = pygame.image.load("themeZo.png")
font = pygame.font.SysFont("arial", 25)
biggerFont = pygame.font.SysFont("papyrus", 40)
mediumFont = pygame.font.SysFont("arial", 30)
currentRecords = []
noRecords = 0
clock = pygame.time.Clock()

pos1 = [(0,0), (150, 0), (0, 40), 0, 40]
pos2 = [(600, 0), (750, 0), (600, 40), 600, 40]

blue = (10, 11, 150)
yellow = (241, 196, 15)
orange = (186, 74, 0)
silver = (120, 120, 120)
green = (35, 155, 86)
bronze = (151, 75, 0)
red = (255, 0, 0)
purple = (200, 0, 210)
white = (255, 255, 255)
first = ""
second = ""
placeholder = "placeholder"
home = HomeIcon()
rate = 60
randomColor = []
status = 10
boss_frequency = 1000
bullets = []
zombies = []
zombie_speed = 0.2
score = 0

for i in range(12):
    randomColor.append(random.randint(70, 170))

def boundaries():
    pygame.draw.line(screen, white,  (0, 60), (0, 600), 5)
    pygame.draw.line(screen, white,  (0, 60), (1200, 60), 5)
    pygame.draw.line(screen, white,  (0, 600), (1200, 600), 5)
    pygame.draw.line(screen, white,  (1200, 60), (1200, 600), 5)

def scoreBoard():
    pygame.draw.rect(screen, white, (0, 0), (1200, 60))

def renderNest():
    pygame.draw.circle(screen, (randomColor[0], randomColor[7], randomColor[8]), (0, 60), 20)
    pygame.draw.circle(screen, (randomColor[1], randomColor[6], randomColor[9]), (0, 600), 20)
    pygame.draw.circle(screen, (randomColor[2], randomColor[5], randomColor[10]), (1200, 600), 20)
    pygame.draw.circle(screen, (randomColor[3], randomColor[4], randomColor[11]), (1200, 60), 20)

def distance(firstX, firstY, secondX, secondY):
    return math.sqrt((firstX - secondX)**2 + (firstY - secondY)**2)

def captionMousePos(mouse_x, mouse_y):
    pygame.set_caption(str(str(mouse_x)+" "+ str(mouse_y)))

def printWithMed(x, y, color, text):
    screen.blit(mediumFont.render(text, True, color), (x, y))

def printWithBig(x, y, color, text):
    screen.blit(biggerFont.render(text, True, color), (x, y))

def giveY():
    if random.randint(0, 1) == 0:
        return 70
    else:
        return 590

def pressableReg(a, b, c, d):
    if x > a and x < b:
        if y > c and y < d:
            return True
    return False
def typing(control, v):
    if control > 30:
        first += v
        return True
    return False

def topNumKills():
    noKillsList = dataList
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].numKills < noKillsList[j+1].numKills:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Player("***", "***", "***", "***", "***"))
    return  noKillsList

def topNumKillsOne():
    noKillsList = list()
    for item in list(dataList):
        if item.controls == 1:
            noKillsList.append(item)
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].numKills < noKillsList[j+1].numKills:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Player("***", "***", "***", "***", "***"))
    return  noKillsList


def topNumKillsTwo():
    noKillsList = list()
    for item in list(dataList):
        if item.controls == 2:
            noKillsList.append(item)
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].numKills < noKillsList[j+1].numKills:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Player("***", "***", "***", "***", "***"))
    return  noKillsList

def topAccuracy():
    noKillsList = dataList
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].accuracy < noKillsList[j+1].accuracy:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Player("***", "***", "***", "***", "***"))
    return  noKillsList

def topAccuracyOne():
    noKillsList = list()
    for item in list(dataList):
        if item.controls == 1:
            noKillsList.append(item)
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].accuracy < noKillsList[j+1].accuracy:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Records("***", "***", "***", "***", 1))
    return  noKillsList

def topAccuracyTwo():
    noKillsList = list()
    for item in list(dataList):
        if item.controls == 2:
            noKillsList.append(item)
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].accuracy < noKillsList[j+1].accuracy:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Records("***", "***", "***", "***", 2))
    return  noKillsList

def topScore():
    noKillsList = dataList
    for i in range(len(noKillsList)):
        for j in range(len(noKillsList) - 1):
            if noKillsList[j].score < noKillsList[j+1].score:
                holder = noKillsList[j+1]
                noKillsList[j+1] = noKillsList[j]
                noKillsList[j] = holder
    if len(noKillsList) < 10:
        for i in range(10 - len(noKillsList)):
            noKillsList.append(Player("***", "***", "***", "***", "***"))
    return  noKillsList

        
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill(blue)
    renderNest()
    boundaries()
    if status == 10:
        width = str(cover.get_width())
        height = str(cover.get_height())
        x = 0
        y = 0
        if x == 0 and y == 0:
            current = Mouse()
        else:
            current = Mouse(x, y)
        screen.blit(cover, (0, 0))
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(109, 208, 379, 429):
                    status = 0
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        keys = pygame.key.get_pressed()
        if keys[pygame.K_GREATER]:
            status = 0
        if pressableReg(109, 208, 379, 429):
            printWithBig(109, 379, yellow, "PLAY")
        else:
            printWithBig(109, 379, purple, "PLAY")

        if pressableReg(800, 1020, 500, 542):
            printWithBig(800, 500, yellow, "HIGH SCORES")
        else:
            printWithBig(800, 500, purple, "HIGH SCORES")
    if status == 11:
        printWithBig(450, 70, purple, "HIGH SCORES")
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(109, 208, 379, 429):
                    status = 0
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        if pressableReg(50, 214, 150, 179):
            printWithMed(50, 150, purple, "Number of kills")
        else:
            printWithMed(50, 150, red, "Number of kills")
        if pressableReg(450, 614, 150, 179):
            printWithMed(450, 150, purple, "Score")
        else:
            printWithMed(450, 150, red, "Score")
        if pressableReg(80, 244, 200, 229):
            printWithMed(80, 200, purple, "For controller 1")
        else:
            printWithMed(80, 200, red, "For controller 1")

        if pressableReg(80, 244, 250, 279):
            printWithMed(80, 250, purple, "For controller 2")
        else:
            printWithMed(80, 250, red, "For controller 2")

        if pressableReg(50, 214, 300, 329):
            printWithMed(50, 300, purple, "Accuracy")
        else:
            printWithMed(50, 300, red, "Accuracy")

        if pressableReg(80, 244, 350, 379):
            printWithMed(80, 350, purple, "For controller 1")
        else:
            printWithMed(80, 350, red, "For controller 1")

        if pressableReg(80, 244, 400, 429):
            printWithMed(80, 400, purple, "For controller 2")
        else:
            printWithMed(80, 400, red, "For controller 2")
        if pressableReg(890, 960, 470, 500):
            home.color = red
        else:
            home.color = white
        home.draw()
        
        if event.type == MOUSEBUTTONDOWN:
            current = Mouse(*event.pos)
            x = current.x
            y = current.y
            if pressableReg(50, 214, 150, 179):
                status = 21
            if pressableReg(80, 244, 200, 229):
                status = 22
            if pressableReg(80, 244, 250, 279):
                status = 23
            if pressableReg(50, 214, 300, 329):
                status = 24
            if pressableReg(80, 244, 350, 379):
                status = 25
            if pressableReg(80, 244, 400, 429):
                status = 26
            if pressableReg(890, 960, 470, 500):
                status = 10
            if pressableReg(450, 614, 150, 179):
                status = 30
    if status == 30:
        noKillsList = topScore()
        printWithBig(450, 70, purple, "SCORE")

        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].score))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].score))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].score))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].score))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].score))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].score))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].score))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].score))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].score))
        
        home.draw()
    if status == 21:
        noKillsList = topNumKills()
        printWithBig(450, 70, purple, "NUMBER OF KILLS")

        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].numKills))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].numKills))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].numKills))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].numKills))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].numKills))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].numKills))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].numKills))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].numKills))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].numKills))
        
        home.draw()
    if status == 22:
        noKillsList = topNumKillsOne()
        printWithBig(450, 70, purple, "Kill Count, Controller 1")

        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].numKills))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].numKills))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].numKills))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].numKills))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].numKills))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].numKills))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].numKills))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].numKills))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].numKills))
        
        home.draw()
    if status == 23:
        noKillsList = topNumKillsTwo()
        printWithBig(450, 70, purple, "Kill Count, Controller 2")

        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].numKills))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].numKills))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].numKills))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].numKills))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].numKills))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].numKills))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].numKills))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].numKills))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].numKills))
        
        home.draw()
    if status == 24:
        noKillsList = topAccuracy()
        printWithBig(450, 70, purple, "ACCURACY")
        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
                    
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].accuracy))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].accuracy))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].accuracy))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].accuracy))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].accuracy))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].accuracy))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].accuracy))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].accuracy))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].accuracy))
        
       
    if status == 25:
        noKillsList = topAccuracyOne()
        printWithBig(450, 70, purple, "Accuracy, Controller 1")

        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].accuracy))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].accuracy))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].accuracy))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].accuracy))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].accuracy))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].accuracy))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].accuracy))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].accuracy))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].accuracy))
        
        home.draw()
    if status == 26:
        noKillsList = topAccuracyTwo()
        printWithBig(450, 70, purple, "Accuracy, Controller 2")

        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                pygame.display.set_caption(current.print())
                if pressableReg(890, 960, 470, 500):
                    home.color = red
                else:
                    home.color = white
            if event.type == MOUSEBUTTONDOWN:
                current = Mouse(*event.pos)
                x = current.x
                y = current.y
                if pressableReg(800, 1020, 500, 542):
                    status = 11
        printWithBig(400, 150, yellow, noKillsList[0].name)
        printWithBig(800, 150, yellow, str(noKillsList[0].accuracy))

        printWithMed(300, 200, silver, noKillsList[1].name)
        printWithMed(700, 200, silver, str(noKillsList[1].accuracy))
        printWithMed(300, 250, bronze, noKillsList[2].name)
        printWithMed(700, 250, bronze, str(noKillsList[2].accuracy))
        printWithMed(300, 300, green, noKillsList[3].name)
        printWithMed(700, 300, green, str(noKillsList[3].accuracy))
        printWithMed(300, 350, green, noKillsList[4].name)
        printWithMed(700, 350, green, str(noKillsList[4].accuracy))
        printWithMed(300, 400, green, noKillsList[5].name)
        printWithMed(700, 400, green, str(noKillsList[5].accuracy))
        printWithMed(300, 450, green, noKillsList[6].name)
        printWithMed(700, 450, green, str(noKillsList[6].accuracy))
        printWithMed(300, 500, green, noKillsList[7].name)
        printWithMed(700, 500, green, str(noKillsList[7].accuracy))
        printWithMed(300, 550, green, noKillsList[8].name)
        printWithMed(700, 550, green, str(noKillsList[8].accuracy))
        
        home.draw()
    if status == 0:
        first = input("Enter your name, player 1! \n")
        my_player = Player(first, yellow, pos1, 600, 330)
        second = input("Enter your name, player 2! \n")
        player_two = Player(second, purple, pos2, 600, 500)
        status = 1
    if status == 1:
        if random.randint(0, 40) == 1:
            if random.randint(0, boss_frequency) == 10:
                zombies.append(Zombie(10, giveY(), zombie_speed, 3))
            if random.randint(0,1) == 0:
                zombies.append(Zombie(10, giveY(), zombie_speed, 1))
            else:
                zombies.append(Zombie(1190, giveY(), zombie_speed, 1))
    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            my_player.moveUp()
        if keys[pygame.K_DOWN]:
            my_player.moveDown()
        if keys[pygame.K_LEFT]:
            my_player.moveLeft()
        if keys[pygame.K_RIGHT]:
            my_player.moveRight()
        if keys[pygame.K_n]:
            my_player.rotateGunLeft()
        if keys[pygame.K_m]:
            my_player.rotateGunRight()
        if keys[pygame.K_SPACE] and my_player.reload > 60:
            my_player.reload = -1
            my_player.numShots += 1
            gun_range = 20
            x = my_player.x + gun_range*math.cos(my_player.angle)
            y = my_player.y + gun_range*math.sin(my_player.angle)
            if my_player.counter != 7:
                i = Bullet(x, y, 5, my_player.angle, my_player, orange, 10)
                bullets.append(i)
            else:
                i = Bullet(x, y, 20, my_player.angle, my_player, red, 40)
                bullets.append(i)

        if keys[pygame.K_w]:
            player_two.moveUp()
        if keys[pygame.K_s]:
            player_two.moveDown()
        if keys[pygame.K_a]:
            player_two.moveLeft()
        if keys[pygame.K_d]:
            player_two.moveRight()
        if keys[pygame.K_1]:
            player_two.rotateGunLeft()
        if keys[pygame.K_2]:
            player_two.rotateGunRight()
        if keys[pygame.K_x] and player_two.reload > 60:
            player_two.reload = -1
            player_two.numShots += 1
            gun_range = 20
            x = player_two.x + gun_range*math.cos(player_two.angle)
            y = player_two.y + gun_range*math.sin(player_two.angle)
            if player_two.counter != 7:
                i = Bullet(x, y, 5, player_two.angle, player_two, orange, 10)
                bullets.append(i)
            else:
                i = Bullet(x, y, 20, player_two.angle, player_two, red, 40)
                bullets.append(i)
                player_two.counter = 0
        if not player_two.isDead():
            player_two.reload += 1
            player_two.draw()
        if not my_player.isDead():
            my_player.reload += 1
            my_player.draw()
        my_player.renderInfo()
        player_two.renderInfo()
        
        if my_player.color == red:
            my_player.color = yellow
        if player_two.color == red:
            player_two.color = purple
        
        for zombie in list(zombies):
            zombie.move()
            zombie.draw()
            zombie.damages(my_player)
            zombie.damages(player_two)
            if my_player.health < 0:
                my_player.health = 0
            if player_two.health < 0:
                player_two.health = 0
        
        for item in list(bullets):
            item.draw()
            item.move()
            for zombie in list(zombies):
                if distance(zombie.x, zombie.y, item.x, item.y)< zombie.radius + item.d:
                    zombie.health -= 1
                    if zombie.health == 0:
                        zombies.remove(zombie)
                        boss_frequency -= 1
                    item.player.score += 100*zombie.speed
                    item.player.counter += 1
                    item.player.numKills += 1
                    zombie_speed += 0.01
                    if item not in bullets:
                        continue
                    else:
                        if item.d != 20:
                            bullets.remove(item)
                        else:
                            continue
            if item.hit():
                if item not in bullets:
                    continue
                else:
                    bullets.remove(item)
        if my_player.health == 0 and player_two.health == 0:
            f  = open("gameDB.py", "a")
            if my_player.numShots == 0:
                my_player.numShots += 0.00001
            if player_two.numShots == 0:
                player_two.numShots += 0.00001
                
            firstAccuracy = round((my_player.numKills / my_player.numShots)*100, 2)
            if firstAccuracy > 100:
                firstAccuracy = 100.00
            secondAccuracy = round((player_two.numKills / player_two.numShots)*100, 2)
            if secondAccuracy > 100:
                secondAccuracy = 100.00
            f.write("dataList.append(Records('"+first+"',"+str(round(my_player.score, 2))+","+str(my_player.numKills)+","+str(firstAccuracy) + ",1)) \n")
            f.write("dataList.append(Records('"+second+"',"+str(round(player_two.score, 2))+","+str(player_two.numKills)+","+str(secondAccuracy) + ",2)) \n")
            f.close()
            status = 2
    if status == 2:
        if my_player.score > player_two.score:
            winner = first
        else:
            winner = second
        statement = winner+ " wins!"

        firstAccuracy = round((my_player.numKills / my_player.numShots)*100, 2)
        if firstAccuracy > 100:
            firstAccuracy = 100.00
        secondAccuracy = round((player_two.numKills / player_two.numShots)*100, 2)
        if secondAccuracy > 100:
            secondAccuracy = 100.00
        screen.blit(biggerFont.render("Game over!", True, white), (450, 0))
        screen.blit(biggerFont.render(statement, True, white), (450, 70))
        
        screen.blit(biggerFont.render("Stats", True, white), (20, 100))
        screen.blit(mediumFont.render(first, True, white), (220, 150))
        screen.blit(mediumFont.render(second, True, white), (720, 150))

        screen.blit(biggerFont.render("Score", True, white), (20, 200))
        screen.blit(font.render(str(my_player.score), True, white), (220, 230))
        screen.blit(font.render(str(player_two.score), True, white), (720, 230))
        
        screen.blit(biggerFont.render("Kills", True, white), (20, 250))
        screen.blit(font.render(str(my_player.numKills), True, white), (220, 280))
        screen.blit(font.render(str(player_two.numKills), True, white), (720, 280))

        screen.blit(biggerFont.render("Accuracy", True, white), (20, 300))
        screen.blit(font.render(str(firstAccuracy) + " %", True, white), (220, 330))
        screen.blit(font.render(str(secondAccuracy) + " %", True, white), (720, 330))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_k]:
            status = 1
            zombies = []
            items = []
            my_player = 1000
            player_two = 1000
    pygame.display.update()

    # Set game clock
    clock.tick(rate)

# Quit Pygame
pygame.quit()    
