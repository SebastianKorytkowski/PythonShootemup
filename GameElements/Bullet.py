import pygame
import Globals
from Utility.SpriteSheet import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, center=None, bullet_type = 0):
        super(Bullet, self).__init__()

        if bullet_type <= 0 or bullet_type > 3:
            bullet_type = 0

        self.surf = Globals.spriteManager.get_sprite_sheet("laser-bolts.png").images[bullet_type]

        self.rect = self.surf.get_rect(center=center)
        self.speed = speed
        self.bullet_type = bullet_type

    def update(self, screen_rect):
        self.rect.move_ip(self.speed)
        if not self.rect.colliderect(screen_rect):
            self.kill()
