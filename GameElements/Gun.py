import Globals


class Gun:
    def __init__(self, gun_type=0, shoot_delay=5):
        self.shoot_previous_frame = 0
        self.shoot_delay_frames = shoot_delay
        self.gun_type = gun_type

    def upgrade(self, levels):
        self.gun_type += levels

    def __spawnBullet(self, direction, position, bullet_type, is_player):
        new_bullet = Globals.Bullet(direction, position, bullet_type=bullet_type, is_player=is_player)
        Globals.game.addBullet(new_bullet, player=is_player)

    def shoot(self, position, is_player):
        if Globals.game.current_frame - self.shoot_previous_frame > self.shoot_delay_frames:
            self.shoot_previous_frame = Globals.game.current_frame

            if is_player:
                dir = -4
            else:
                dir = 3

            nr_of_bullets = self.gun_type % 3 + 1
            bullet_type = int(self.gun_type/3)

            if nr_of_bullets == 1:
                self.__spawnBullet((0, dir), position, bullet_type, is_player)
            elif nr_of_bullets == 2:
                self.__spawnBullet((-1, dir), position, bullet_type, is_player)
                self.__spawnBullet((1, dir), position, bullet_type, is_player)
            else:
                self.__spawnBullet((-2, dir), position, min(1, bullet_type), is_player)
                self.__spawnBullet((0, dir), position, bullet_type, is_player)
                self.__spawnBullet((2, dir), position, min(1, bullet_type), is_player)

            Globals.resourceManager.get_sound("shot-heavy.wav").play()
