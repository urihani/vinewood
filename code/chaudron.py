import pygame
from settings import *
from support import *
from interactable import Interactable


class Chaudron(Interactable):
    def __init__(self, pos, groups, obstacle_sprites):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'chaudron'

        main_path = '../graphics/cauldron/'
        self.animation = import_folder(main_path)

        # graphics setup
        self.image = self.animation[self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

    def animate(self):

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0

        self.image = self.animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
