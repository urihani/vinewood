import math
import sys
import pygame
from math import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        self.speed = 10
        self.x = x
        self.y = y

        # vitesses
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
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
