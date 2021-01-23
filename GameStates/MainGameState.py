from pygame import VIDEORESIZE, HWSURFACE, DOUBLEBUF, RESIZABLE

from GameElements.BaseClasses.DrawableAnimation import Animation
from GameElements.Player import *
from GameElements.Background import *
from GameStates.GameState import GameState
from Gui.GuiBar import GuiBar
from Gui.GuiText import GuiText
from Level import *


class MainGameState(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.resetGame()

    def resetGame(self):
        self.player = Player((Globals.window.screen_size[0] / 2, Globals.window.screen_size[1]))
        self.level = Level(self)

        self.score = 0

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.foreground = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()



        # GUI
        self.gui = pygame.sprite.Group()
        self.hp_bar = GuiBar(pygame.Rect(5, 5, 128, 16))
        self.score_text = GuiText(position=(5, 16+5+5), font_size=16)
        self.gui.add(self.hp_bar)
        self.gui.add(self.score_text)

        self.level.Start()

    def addEnemy(self, new_enemy):
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def spawnExplosion(self, position):
        new_explosion = Animation(Globals.resourceManager.get_sprite_sheet("explosion.png"), center=position,
                                  loop=False, frames_per_frame=5)
        self.effects.add(new_explosion)

    def addBackground(self, image) -> Background:
        new_background = Background(image)
        self.background.add(new_background)
        return new_background

    def addForeground(self, image) -> Background:
        new_foreground = Background(image)
        self.foreground.add(new_foreground)
        return new_foreground

    def addBullet(self, bullet, player=True):
        if player:
            self.player_bullets.add(bullet)
        else:
            self.enemy_bullets.add(bullet)
        self.all_sprites.add(bullet)

    @staticmethod
    def pixel_perfect_collision(s1, s2):
        # First check rect collision then check mask collision
        return s1.rect.colliderect(s2) and pygame.sprite.collide_mask(s1, s2)

    def check_collisions(self):

        for powerup in self.powerups:
            # Check if player picked up a powerup
            if self.player.rect.colliderect(powerup.rect):
                powerup.on_pickup(self.player)
                powerup.kill()
                Globals.resourceManager.get_sound("powerup.wav").play()

        for enemy in self.enemies:
            # Check if enemy is hit by a bullet
            for bullet in self.player_bullets:
                if self.pixel_perfect_collision(bullet, enemy):
                    enemy.damage(bullet.get_dmg())
                    bullet.kill()
                    Globals.resourceManager.get_sound("hit.wav").play()
                    Globals.window.shakeCamera(1)
            # Check if enemy is hit by the player
            if self.player.is_alive() and not self.player.is_invincible() and self.pixel_perfect_collision(self.player, enemy):
                self.player.damage(50)
                enemy.damage(50)
                Globals.resourceManager.get_sound("hit.wav").play()
                Globals.window.shakeCamera(5)

        if self.player.is_alive() and not self.player.is_invincible():
            for enemy_bullet in self.enemy_bullets:
                if self.pixel_perfect_collision(self.player, enemy_bullet):
                    self.player.damage(enemy_bullet.get_dmg())
                    enemy_bullet.kill()
                    Globals.resourceManager.get_sound("hit.wav").play()
                    Globals.window.shakeCamera(5)

    def start(self):
        self.level.Start()

    def end(self):
        pass

    def update(self):
        screen_rect = Globals.window.fake_screen.get_rect()

        if self.player.is_alive():
            move = self.level.Update()
            # update player and his bullets
            pressed_keys = pygame.key.get_pressed()
            self.player.update(screen_rect, pressed_keys)
            self.player_bullets.update(screen_rect)
        else:
            move = self.level.Update(player_alive=False)

        # update enemies and their bullets
        self.enemies.update(screen_rect)
        self.enemy_bullets.update(screen_rect)

        # move backgrounds
        self.background.update(move, screen_rect)

        # move foreground
        self.foreground.update(move * 2, screen_rect)
        self.effects.update(move * 2, screen_rect)
        self.powerups.update(move * 2, screen_rect)

        self.check_collisions()

    def draw(self, screen):
        # draw background
        for entity in self.background:
            entity.draw(screen)
        # draw foreground clouds etc.
        for entity in self.foreground:
            entity.draw(screen)
        # draw effects explosions etc.
        for entity in self.effects:
            entity.draw(screen)
        # draw powerups
        for entity in self.powerups:
            entity.draw(screen)
        # draw all generic sprites enemies, player, etc.
        for entity in self.all_sprites:
            entity.draw(screen)
        # sync and draw gui
        self.score_text.set_text("SCORE: " + str(self.score))
        self.hp_bar.set_progress(self.player.hp / self.player.max_hp)
        for entity in self.gui:
            entity.draw(screen)


