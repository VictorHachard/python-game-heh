import pygame, sys, math, random
from settings import *
from pygame import locals as const
from button import Button

class Game(object):
    """docstring for Game."""

    array_colors = [['red', RED], ['blue', BLUE], ['green', GREEN], ['orange', ORANGE], ['yellow', YELLOW]]

    def __init__(self, row, colum, radius, screen):
        super(Game, self).__init__()
        self.screen = screen
        self.row = row
        self.colum = colum
        self.radius = radius
        self.array_circle = []
        self.array_button = []
        self.array_secret = []
        self.array_secret2 = []
        self.j = 0

    def start(self):
        self.array_button.append(['Enter', Button(self.screen).createButton([100, 440], 'Enter', 60).render()])
        self.array_button.append(['Menu', Button(self.screen).createButton([250, 440], 'Menu', 60).render()])
        secrets = random.sample(range(0, len(self.array_colors) - 1), self.row)
        for secret in secrets:
            self.array_secret.append([self.array_colors[secret][0], ''])
            self.array_secret2.append(self.array_colors[secret][0])
        for j in range(self.colum):
            self.array_circle.append([])
            for i in range(self.row):
                self.createCircle(j, i)
        print(str(self.array_secret2).strip('[]'))
        return self

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            return self.mouse(pygame.mouse.get_pos(), event.button == 3 if True else False)

    def mouse(self, pos, right):
        for circle in self.array_circle[self.j]:
            sqx = (pos[0] - circle[0])**2
            sqy = (pos[1] - circle[1])**2
            if math.sqrt(sqx + sqy) < self.radius:
                if right:
                    if circle[2] == 'grey':
                        circle[2] = self.array_colors[len(self.array_colors) - 1][0]
                        pygame.draw.circle(self.screen, self.array_colors[len(self.array_colors) - 1][1], (circle[0], circle[1]), self.radius)
                        return
                    else:
                        i = 0
                        for color in self.array_colors:
                            if circle[2] == color[0]:
                                circle[2] = self.array_colors[i-1][0]
                                pygame.draw.circle(self.screen, self.array_colors[i-1][1], (circle[0], circle[1]), self.radius)
                                return
                            i = i + 1
                else:
                    if circle[2] == 'grey':
                        circle[2] = self.array_colors[0][0]
                        pygame.draw.circle(self.screen, self.array_colors[0][1], (circle[0], circle[1]), self.radius)
                        return
                    else:
                        i = 0
                        for color in self.array_colors:
                            if circle[2] == color[0]:
                                if i+1 >= len(self.array_colors):
                                    circle[2] = self.array_colors[0][0]
                                    pygame.draw.circle(self.screen, self.array_colors[0][1], (circle[0], circle[1]), self.radius)
                                    return
                                else:
                                    circle[2] = self.array_colors[i+1][0]
                                    pygame.draw.circle(self.screen, self.array_colors[i+1][1], (circle[0], circle[1]), self.radius)
                                    return
                            i = i + 1
        for button in self.array_button:
            if  button[0] == 'Menu' and button[1].isMouseIn(pos):
                return False
            if button[0] == 'Enter' and button[1].isMouseIn(pos):
                for secret in self.array_secret:
                    secret[1] = ''
                print(self.array_secret)
                for circle in self.array_circle[self.j]:
                    if circle[2] == 'grey':
                        return
                place = 0
                i = 0
                for circle in self.array_circle[self.j]:
                    if circle[2] == self.array_secret[i][0]:
                        # print('bien ' + circle[2] + ' ' + self.array_secret[i][0])
                        place = place + 1
                        self.array_secret[i][1] = 'bien'
                    i = i + 1
                present = 0
                for circle in self.array_circle[self.j]:
                    for secret in self.array_secret:
                        if secret[1] != 'bien' and secret[0] == circle[2]:
                            # print(secret[0] + ' ' + circle[2])
                            present = present + 1
                marginY = int(self.j * 80 + 20)
                font = pygame.font.SysFont('comicsans', 20)
                text = font.render('Bon: ' + str(place), 1, WHITE)
                self.screen.blit(text, (560, marginY))
                text = font.render('Là : ' + str(present), 1, WHITE)
                self.screen.blit(text, (560, marginY + 10))
                self.j = self.j + 1
                if (place == self.row): #win
                    return True
                if (self.j >= self.colum): #lose
                    return False

        return

    def createCircle(self, j, i):
        marginX = int((HEIGHT - (self.radius * self.row)) / (self.row + 1))
        marginY = int((WIDTH - (self.radius * self.colum)) / (self.colum + 1))
        self.array_circle[j].append([marginX + i * (marginX + self.radius), marginY + j * (marginY + self.radius), 'grey', ''])
        pygame.draw.circle(self.screen, GREY, (self.array_circle[j][i][0], self.array_circle[j][i][1]), self.radius)