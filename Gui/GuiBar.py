import pygame

from GameElements.BaseClasses.DrawableSprite import DrawableSprite


class GuiBar(DrawableSprite):
    def __init__(self, size: pygame.Rect, progress=1.0, color=(0, 255, 0), back_color=(0, 0, 0), padding=1):
        DrawableSprite.__init__(self)

        self.rect = size
        self.progress = progress
        self.color = color
        self.back_color = back_color
        self.padding = padding

    # from 0 to 1
    def set_progress(self, progress):
        self.progress = progress

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.rect, border_radius=2)
        pygame.draw.rect(surface, self.color,
                         pygame.Rect(self.rect.left + self.padding,
                                     self.rect.top + self.padding,
                                     (self.rect.width - self.padding * 2) * self.progress,
                                     (self.rect.height - self.padding * 2)),
                         border_radius=2)
