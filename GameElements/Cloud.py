import pygame

import Globals


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = Globals.spriteManager.get_image("cloud.png")

        self.rect = self.surf.get_rect()
        self.rect.bottom = 0

    def update(self, screen_rect):
        self.rect.move_ip(0, 5)
        if not self.rect.colliderect(screen_rect):
            self.kill()
