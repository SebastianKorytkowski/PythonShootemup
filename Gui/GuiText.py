import pygame
import pygame.freetype

from GameElements.BaseClasses.DrawableSprite import DrawableSprite
from Utility import Globals


class GuiText(DrawableSprite):
    def __init__(self, text="", position=None, color=(255, 255, 255), font_size=24):
        DrawableSprite.__init__(self)
        self.text = text
        self.font_size = font_size
        self.position = position
        self.color = color
        self.font = Globals.resourceManager.get_font("Sprites/font.ttf", self.font_size)

        self.set_text(text)

    def __render__(self):
        self.surf, self.rect = self.font.render(self.text, self.color)

    # from 0 to 1
    def set_text(self, text):
        self.text = text
        self.__render__()

        if self.position is not None:
            self.rect.top = self.position[1]
            self.rect.left = self.position[0]

    def draw(self, surface):
        surface.blit(self.surf, self.rect)

