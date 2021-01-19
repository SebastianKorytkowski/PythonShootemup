import pygame
import random
import Globals


class EnemyAILine:
    def __init__(self, AI_dir=(0, 1)):
        self.AI_dir = pygame.Vector2(AI_dir).normalize()

    def move_direction(self, enemy):
        return self.AI_dir


class EnemyAIFlyby:
    def move_direction(self, enemy):
        diff = Globals.game.player.pos - enemy.pos

        if diff.y > 100:
            return pygame.Vector2(diff.x, 50).normalize()
        elif enemy.speed.x > 0.0:
            enemy.ai = EnemyAILine((1, 1))
        else:
            enemy.ai = EnemyAILine((-1, 1))

        if diff.x != 0:
            return pygame.Vector2(diff.x, 0).normalize()
        else:
            return pygame.Vector2(0, 0)


class EnemyAIHover:
    def move_direction(self, enemy):
        diff = Globals.game.player.pos - enemy.pos

        target = 20 + enemy.rect.height
        tolerance = 5

        if enemy.pos.y < target - tolerance:
            return pygame.Vector2(diff.x, 50).normalize()
        elif enemy.pos.y > target + tolerance:
            return pygame.Vector2(diff.x, -50).normalize()
        elif abs(diff.x) > 2.0:
            return pygame.Vector2(diff.x, 0).normalize()
        else:
            return pygame.Vector2(0, 0)


class EnemyAISuicide:
    def move_direction(self, enemy):
        diff = Globals.game.player.pos - enemy.pos


        #if diff.magnitude_squared()>enemy.bomb_range:
        if abs(diff.x) > 2.0:
            return pygame.Vector2(diff.x, 300).normalize()
        else:
            return pygame.Vector2(0, 1)
        #else:
        #    # Commit suicide
        #    enemy.damage(enemy.hp)
        #    return pygame.Vector2(0, 0)


def move_to_target(pos, targetpos, tolerance):
    diff = targetpos - pos
    x = abs(diff.x) > tolerance
    y = abs(diff.y) > tolerance
    if x and y:
        return diff.normalize()
    elif x:
        return pygame.Vector2(diff.x, 0).normalize()
    elif y:
        return pygame.Vector2(0, diff.y).normalize()
    else:
        return pygame.Vector2(0, 0)


class EnemyAIFormation:
    def __init__(self, target, AI_on_target_death=EnemyAIFlyby()):
        self.AI_target = target
        self.AI_on_target_death = AI_on_target_death

    def move_direction(self, enemy):
        if self.AI_target.hp != 0:
            tmp = move_to_target(enemy.pos, self.AI_target.pos + pygame.Vector2(-self.AI_target.rect.width,
                                                                                self.AI_target.rect.height / 2), 10)
            return tmp
        else:
            enemy.ai = self.AI_on_target_death
            return pygame.Vector2(0, 0)
