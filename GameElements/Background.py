import pygame

import Globals


class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Background, self).__init__()
        self.surf = image

        self.rect = self.surf.get_rect()
        self.rect.bottom = 0

    def update(self, move, screen_rect):
        self.rect.move_ip(0, move)
        if not self.rect.colliderect(screen_rect):
            self.kill()
