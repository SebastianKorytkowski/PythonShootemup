from pygame.mixer import Sound

from Utility.SpriteSheet import *
from pygame.locals import RLEACCEL


class ResourceManager:
    def __init__(self, spriteFolder, soundFolder):
        self.spriteSheets = dict()
        self.images = dict()
        self.sounds = dict()
        self.fonts = dict()
        self.spiteFolder = spriteFolder
        self.soundFolder = soundFolder

    def get_sound(self, filename) -> Sound:
        try:
            return self.sounds[filename]
        except KeyError:
            sound = pygame.mixer.Sound(self.soundFolder + filename)
            sound.set_volume(0.01)
            self.sounds[filename] = sound
            return sound

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

    def get_font(self, filename, size):
        try:
            return self.fonts[(filename, size)]
        except KeyError:
            font = pygame.freetype.Font(filename, size)
            self.fonts[(filename, size)] = font
            return font