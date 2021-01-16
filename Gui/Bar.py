import pygame


class Bar:
    def __init__(self, size:pygame.Rect, progress=1.0, color=(0, 255, 0)):
        self.size = size
        self.progress = progress
        self.color = color

    # from 0 to 1
    def setProgress(self, progress):
        self.progress = progress

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.size.left, self.size.top, self.size.width * self.progress, self.size.height))
