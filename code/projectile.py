import math
import sys
import pygame
from math import *
from settings import *
from support import import_folder


class Projectile(pygame.sprite.Sprite):
    def __init__(self, groups, sprites, x, y, angle):
        pygame.sprite.Sprite.__init__(self, groups)
        self.current_sprite = 0
        self.sprites = sprites
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x-20
        self.rect.y = y-20
        self.angle = angle
        self.x = x
        self.y = y
        self.x_dist = 1
        self.y_dist = 1

        # stats
        self.speed = powers_data['fire_ball']['speed']
        self.reach = powers_data['fire_ball']['reach']

        # vitesses
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

        self.deg = math.degrees(self.angle)
        # print(self.deg)

    def update(self):
        self.animate()
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Les codes ci dessous sont temporaire, celui de Ju sera bon pour la suite,
        # mais j'ai rencontré des bugs avec le déplacement de la caméra. J'ai implémenté un workaround. Loïc

        # portée des projectiles
        self.x_dist += 1
        self.y_dist += 1

        # CODE DE JU
        #self.x_dist = self.rect.x - (1024 / 2)
        #self.y_dist = self.rect.y - (768 / 2)

        self.dist = math.hypot(self.x_dist, self.y_dist)
        
        # CODE DE JU
        #if self.dist > self.reach:

        if self.dist > 120:
            self.kill()

    def animate(self):
        self.current_sprite += 0.3

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
        self.image = pygame.transform.rotate(self.image, self.deg)
