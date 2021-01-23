import pygame
from enum import Enum

from GameElements.Bullet import Bullet
from Utility import Globals


class Bullets(Enum):
    STARING_BULLET = 1
    MAX_BULLET = 4*3
    ROCKET = 64

class Gun:
    def __init__(self, gun_type=0, shoot_delay=5, bullet_speed=3, special_offset=None,):
        self.shoot_previous_frame = 0
        self.shoot_delay_frames = shoot_delay
        self.gun_type = gun_type
        self.bullet_speed = bullet_speed
        self.special_offset = special_offset

    def upgrade(self, levels):
        self.gun_type += levels

    def __spawnBullet(self, direction, position, bullet_type, is_player):
        new_bullet = Bullet(direction, position, bullet_type=bullet_type, is_player=is_player)
        Globals.game.addBullet(new_bullet, player=is_player)

    def __spawnRocket(self, position):
        new_rocket = Globals.game.level.create_enemy(3);
        new_rocket.pos = pygame.Vector2(position)
        Globals.game.addEnemy(new_rocket)

    def shoot(self, shooter, is_player):
        if Globals.window.current_frame - self.shoot_previous_frame > self.shoot_delay_frames:
            self.shoot_previous_frame = Globals.window.current_frame

            position = list(shooter.rect.center)

            if is_player:
                yspeed = -self.bullet_speed
            else:
                yspeed = self.bullet_speed

            if self.special_offset is None:
                if is_player:
                    position[1] -= shooter.rect.height / 2
                else:
                    position[1] += shooter.rect.height / 2
            else:
                position[0] += (shooter.rect.width  / 2)*self.special_offset[0]
                position[1] += (shooter.rect.height / 2)*self.special_offset[1]

            if self.gun_type == Bullets.ROCKET:
                self.__spawnRocket(position)
                return

            if self.gun_type>=4*3:
                self.gun_type = 4*3-1

            nr_of_bullets = self.gun_type % 3 + 1
            bullet_type = int(self.gun_type/3)

            if nr_of_bullets == 1:
                self.__spawnBullet((0, yspeed), position, bullet_type, is_player)
            elif nr_of_bullets == 2:
                self.__spawnBullet((-1, yspeed), position, bullet_type, is_player)
                self.__spawnBullet((1, yspeed), position, bullet_type, is_player)
            else:
                self.__spawnBullet((-2, yspeed), position, min(1, bullet_type), is_player)
                self.__spawnBullet((0, yspeed), position, bullet_type, is_player)
                self.__spawnBullet((2, yspeed), position, min(1, bullet_type), is_player)

            Globals.resourceManager.get_sound("shot-heavy.wav").play()
