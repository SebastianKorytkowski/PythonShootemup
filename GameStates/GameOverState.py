import pygame

from Gui.GuiText import GuiText
from Utility import Globals


class GameOverState:
    def __init__(self, game_state):
        self.game_state = game_state

        self.text = GuiText("GAME OVER", font_size=30)
        self.text.rect.center = (Globals.window.screen_size[0]/2, Globals.window.screen_size[1]/2)

        self.gui = pygame.sprite.Group()
        self.gui.add(self.text)

    def start(self):
        pass

    def end(self):
        pass

    def update(self):
        self.game_state.update()
        pressed_keys = pygame.key.get_pressed()
        pass

    def draw(self, screen):
        self.game_state.draw(screen)
        for entity in self.gui:
            entity.draw(screen)
