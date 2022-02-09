import pygame
from support import *


class Cauldron(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos = pos
        self.sprites = import_folder('../graphics/cauldron/')
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(0, -10)

    def animate(self):
        self.current_sprite += 0.3

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

    def update(self):
        self.animate()
