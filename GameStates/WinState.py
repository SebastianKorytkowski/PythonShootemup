import pygame

from Gui.GuiText import GuiText
from Utility import Globals

from pygame.locals import (
    K_r
)

class WinState:
    def __init__(self, game_state):
        self.game_state = game_state

        self.text1 = GuiText("YOU WIN!!!", font_size=30)
        self.text1.rect.center = (Globals.window.screen_size[0]/2, Globals.window.screen_size[1]/2)

        self.text2 = GuiText("SCORE:" + str(self.game_state.score), font_size=30)
        self.text2.rect.center = (Globals.window.screen_size[0]/2, Globals.window.screen_size[1]/2+35)

        self.text3 = GuiText("PRESS R TO RESTART", font_size=30)
        self.text3.rect.center = (Globals.window.screen_size[0]/2, Globals.window.screen_size[1]/2+70)

        self.gui = pygame.sprite.Group()
        self.gui.add(self.text1)
        self.gui.add(self.text2)
        self.gui.add(self.text3)

    def start(self):
        self.game_state.gui.empty()
        pass

    def end(self):
        pass

    def update(self):
        self.game_state.update()
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_r]:
            from GameStates.MainGameState import MainGameState
            Globals.window.change_game_state(MainGameState())

        pass

    def draw(self, screen):
        self.game_state.draw(screen)
        for entity in self.gui:
            entity.draw(screen)
