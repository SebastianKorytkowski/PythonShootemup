import pygame
import random
import Globals



class EnemyAILine:
    def __init__(self, AI_dir=(0, 1)):
        self.AI_dir = pygame.Vector2(AI_dir).normalize()

    def move_direction(self, enemy):
        return self.AI_dir

class EnemyAIFollow:
    def move_direction(self, enemy):
        diff = Globals.game.player.pos-enemy.pos

        if diff.y > 100:
            return pygame.Vector2(diff.x, 50).normalize()
        elif enemy.speed.x>0.0:
            enemy.ai = EnemyAILine((1, 1))
        else:
            enemy.ai = EnemyAILine((-1, 1))

        return pygame.Vector2(diff.x, 0).normalize()
