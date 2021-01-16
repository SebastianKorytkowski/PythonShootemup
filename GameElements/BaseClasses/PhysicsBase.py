import pygame


class PhysicsBase:
    def __init__(self, speed=(0, 0), pos=None):
        self.speed = pygame.math.Vector2(speed)
        if pos is not None:
            self.pos = pygame.math.Vector2(pos)
        else:
            self.pos = pygame.math.Vector2(self.rect.center)

    def update_physics(self):
        self.pos += self.speed
        self.rect.center = self.pos
