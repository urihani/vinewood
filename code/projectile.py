import math
import sys
import pygame
from math import *
from settings import *
from support import import_folder


class Projectile(pygame.sprite.Sprite):
    def __init__(self, sprites, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.current_sprite = 0
        self.sprites = sprites
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        self.speed = powers_data['fire_ball']['speed']
        self.x = x
        self.y = y

        # vitesses
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

        self.deg = math.degrees(self.angle)
        print(self.deg)

    def update(self):
        self.animate()
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # portée des projectiles
        self.x_dist = self.rect.x - (1024 / 2)
        self.y_dist = self.rect.y - (768 / 2)
        self.dist = math.hypot(self.x_dist, self.y_dist)
        if self.dist > 200:
            self.kill()

    def animate(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
        self.image = pygame.transform.rotate(self.image, self.deg)
