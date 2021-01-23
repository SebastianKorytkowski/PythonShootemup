import pygame

from GameElements.BaseClasses.DrawableSprite import DrawableSprite


class Background(DrawableSprite):
    def __init__(self, image):
        DrawableSprite.__init__(self)
        self.surf = image

        self.rect = self.surf.get_rect()
        self.rect.bottom = 0

    def update(self, move, screen_rect):
        self.rect.move_ip(0, move)
        if not self.rect.colliderect(screen_rect):
            self.kill()
