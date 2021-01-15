import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, center=None):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=center)
        self.speed = 5

    def update(self, screen_rect):
        self.rect.move_ip(0, self.speed)
        if not self.rect.colliderect(screen_rect):
            self.kill()
