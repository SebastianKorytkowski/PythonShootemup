import pygame

import Globals


class Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, center=None, loop=True, frames_per_frame=10):
        super(Animation, self).__init__()
        self.surf = pygame.Surface((20, 10))

        self.sprite_sheet = sprite_sheet
        self.current_frame = 0
        self.loop = loop
        self.frames_per_frame = frames_per_frame

        self.setFrame(0)
        self.rect = self.surf.get_rect(center=center)

    def setFrame(self, nr):
        self.current_frame = nr

        # if out of frames
        if nr < 0 or nr >= len(self.sprite_sheet.images):
            if self.loop:
                self.current_frame = 0
            else:
                self.kill()
                return

        self.surf = self.sprite_sheet.images[self.current_frame]

    def nextFrame(self):
        self.setFrame(self.current_frame+1)

    def update(self):
        if Globals.game.current_frame % self.frames_per_frame == 0:
            self.nextFrame()
