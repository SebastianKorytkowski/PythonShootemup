from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE
import pygame

from GameStates.MainGameState import MainGameState
from Utility import Globals


class Window:
    def __init__(self):
        self.screen_size = (512, 600)

        self.screen = pygame.display.set_mode(self.screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.fake_screen = self.screen.copy()
        self.running = False
        self.game_state = None
        self.current_frame = 0
        self.camera_shake = 0

    def shakeCamera(self, intensity):
        self.camera_shake = abs(self.camera_shake + intensity)

    def setScale(self, scale):
        if scale > 3:
            scale = 3

        self.screen = pygame.display.set_mode((self.screen_size[0] * scale, self.screen_size[1] * scale),
                                              HWSURFACE | DOUBLEBUF | RESIZABLE)

    def change_game_state(self, game_state):
        if self.game_state is not None:
            self.game_state.end()

        self.game_state = game_state

        if type(self.game_state) is MainGameState:
            Globals.game = self.game_state

        if self.game_state is not None:
            self.game_state.start()

    def start(self):
        clock = pygame.time.Clock()
        self.change_game_state(MainGameState())
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Globals.window.running = False
                elif event.type == VIDEORESIZE:
                    width, height = event.size
                    scale = int(max((width / self.screen_size[0], height / self.screen_size[1]))) + 1
                    self.setScale(scale)

            self.game_state.update()
            self.game_state.draw(self.fake_screen)

            # draw the fake screen on the real screen
            self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size),
                             (self.camera_shake, 0))
            self.camera_shake = -self.camera_shake / 2

            pygame.display.flip()

            clock.tick(60)
            self.current_frame += 1