import pygame
from settings import *
from pygame import locals as const
from Items.button import Button
from Items.text import Text
from Menus.game import Game


class Menu(object):
    """docstring for Menu."""

    def __init__(self, screen, main, items, offset = 0):
        self.items = []
        self.item = 0
        self.main = main
        self.screen = screen
        self.height = HEIGHT - (items - offset) * 20 - 40
        self.itemsPos = [(self.height / items * x) for x in range(items)]
        self.itemsPos = [self.itemsPos[x] + 40 for x in range(items)]

    def update(self, event):
        """Update, return the id of the button that colliding with the mouse"""
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # true
                for button in self.items:
                    if button[0] == 'button' and button[1].isMouseIn(pygame.mouse.get_pos()):
                        self.main.effects_sounds['click_button'].play()
                        return button[2]

    def addButton(self, text, id, color = BLACK):
        """Add a button"""
        self.items.append(['button', Button(self.screen, self.main).center().createButton([0, self.itemsPos[self.item]], text, 60, colorText = color), id])
        self.item = self.item + 1
        return self

    def addText(self, text, fontSize = 40, colorText = BLACK):
        """Add a text"""
        self.items.append(['text', Text(self.screen).center().createText([0, self.itemsPos[self.item]], text, fontSize, colorText)])
        self.item = self.item + 1
        return self

    def addImage(self, image, size):
        """Add an image"""
        self.items.append(['image', ForeGroundImage(self.screen, self.main).createImage([-1, self.itemsPos[self.item]], image, size)])
        self.item = self.item + 1
        return self

    def render(self):
        """Render this object, return this"""
        for item in self.items:
            item[1].render()
        return self
