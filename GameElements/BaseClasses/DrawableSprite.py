import pygame


class DrawableSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
