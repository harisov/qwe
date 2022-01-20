import os
import pygame
from pygame.locals import *
import sys
import random


pygame.init()
size = width, height = 600, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Дудл джамп")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Dudu:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)

        self.green = load_image("зеленая.png")
        self.green = pygame.transform.scale(self.green, (90, 30))

        self.blue = load_image("двигается.png")
        self.blue = pygame.transform.scale(self.blue, (90, 30))

        self.red = load_image("сломаная_притворяется.png")
        self.red = pygame.transform.scale(self.red, (90, 30))

        self.red_1 = load_image("сломаная_сломаная.png")
        self.red_1 = pygame.transform.scale(self.red_1, (90, 30))

        self.playerRight = load_image("дудл_3.png", colorkey=-1)
        self.playerRight = pygame.transform.scale(self.playerRight, (80, 80))

        self.playerRight_1 = load_image("дудл_1.png", colorkey=-1)
        self.playerRight_1 = pygame.transform.scale(self.playerRight_1, (80, 80))

        self.playerLeft = load_image("дудл.png", colorkey=-1)
        self.playerLeft = pygame.transform.scale(self.playerLeft, (80, 80))

        self.playerLeft_1 = load_image("дудл_2.png", colorkey=-1)
        self.playerLeft_1 = pygame.transform.scale(self.playerLeft_1, (80, 80))

        self.spring = load_image("пружина.png")
        self.spring = pygame.transform.scale(self.spring, (30, 30))

        self.spring_1 = load_image("пружина_1.png")
        self.spring_1 = pygame.transform.scale(self.spring_1, (30, 30))

        self.direction = 0
        self.gamer_x = 300
        self.gamer_y = 300
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cam = 0
        self.jump = 0
        self.gravity = 0
        self.move_moment = 0

    def updatePlayer(self):
        if not self.jump:
            self.gamer_y += self.gravity
            self.gravity += 1
        elif self.jump:
            self.gamer_y -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.move_moment < 10:
                self.move_moment += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.move_moment > -10:
                self.move_moment -= 1
            self.direction = 1
        else:
            if self.move_moment > 0:
                self.move_moment -= 1
            elif self.move_moment < 0:
                self.move_moment += 1
        if self.gamer_x > 600:
            self.gamer_x = -50
        elif self.gamer_x < -50:
            self.gamer_x = 600
        self.gamer_x += self.move_moment
        if self.gamer_y - self.cam <= 200:
            self.cam -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.gamer_x, self.gamer_y - self.cam))
            else:
                self.screen.blit(self.playerRight, (self.gamer_x, self.gamer_y - self.cam))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.gamer_x, self.gamer_y - self.cam))
            else:
                self.screen.blit(self.playerLeft, (self.gamer_x, self.gamer_y - self.cam))

    def update(self):
        for i in self.platforms:
            rect = pygame.Rect(i[0], i[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.gamer_x, self.gamer_y, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.gamer_y < (i[1] - self.cam):
                if i[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    i[-1] = 1
            if i[2] == 1:
                if i[-1] == 1:
                    i[0] += 5
                    if i[0] > 550:
                        i[-1] = 0
                else:
                    i[0] -= 5
                    if i[0] <= 0:
                        i[-1] = 1

    def drawPlatforms(self):
        for i in self.platforms:
            m = self.platforms[1][1] - self.cam
            if m > 800:
                platform = random.randint(0, 1000)
                if platform < 600:
                    platform = 0
                elif 900 > platform >= 600:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                cords = self.platforms[-1]
                m = random.randint(0, 1000)
                if m > 900 and platform == 0:
                    self.springs.append([cords[0], cords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if i[2] == 0:
                self.screen.blit(self.green, (i[0], i[1] - self.cam))
            elif i[2] == 1:
                self.screen.blit(self.blue, (i[0], i[1] - self.cam))
            elif i[2] == 2:
                if not i[3]:
                    self.screen.blit(self.red, (i[0], i[1] - self.cam))
                else:
                    self.screen.blit(self.red_1, (i[0], i[1] - self.cam))

        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cam))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cam))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(
                    pygame.Rect(self.gamer_x, self.gamer_y, self.playerRight.get_width(),
                                self.playerRight.get_height())):
                self.jump = 50
                self.cam -= 50

    def generatePlatforms(self):
        on = 1000
        while on > -100:
            x = random.randint(0, 600)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif 900 > platform >= 800 :
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, 800))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (800, x * 12))

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill(pygame.Color('white'))
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.gamer_y - self.cam > 700:
                self.cam = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.gamer_x = 400
                self.gamer_y = 400
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.update()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()


Dudu().run()