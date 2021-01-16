import pygame
from pygame.locals import RLEACCEL

class SpriteSheet:
    def __init__(self, filename, width, height):
        self.sheet = pygame.image.load(filename)
        self.width = width
        self.height = height

        self.images = []

        single_sprite_width = int(self.sheet.get_width() / self.width)
        single_sprite_height = int(self.sheet.get_height() / height)

        print(single_sprite_width)
        print(single_sprite_height)

        for y in range(0, height):
            starty = y * single_sprite_height
            for x in range(0, width):
                startx = x * single_sprite_width
                rect = (startx, starty, single_sprite_width, single_sprite_height)
                self.images.append(self.image_at(rect))

        print(filename + " " + str(len(self.images)))

    def get_width(self):
        return self.sheet.get_width() / self.width

    def get_height(self):
        return self.sheet.get_height() / self.height

    def get_at_pos(self, x, y):
        return self.images[y*self.width+x]

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey((0, 0, 0), RLEACCEL)
        return image
