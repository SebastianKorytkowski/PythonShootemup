from Utility.SpriteSheet import *
from pygame.locals import RLEACCEL


class SpriteManager:
    def __init__(self, spriteFolder):
        self.spriteSheets = dict()
        self.images = dict()
        self.spiteFolder = spriteFolder

    def load_sprite_sheet(self, filename, width, height) -> None:
        self.spriteSheets[filename] = SpriteSheet(self.spiteFolder + filename, width, height)

    def get_sprite_sheet(self, filename) -> SpriteSheet:
        return self.spriteSheets[filename]

    def get_image(self, filename) -> pygame.surface:
        try:
            return self.images[filename]
        except KeyError:
            image = pygame.image.load(self.spiteFolder + filename).convert_alpha()
            image.set_colorkey((0, 0, 0), RLEACCEL)
            self.images[filename] = image
            return image
