import math
from tkinter.messagebox import NO
from tkinter.ttk import Style
import pygame
from settings import *
from support import import_folder
from entity import Entity
from projectile import *


class Hero(Entity):
    def __init__(self, pos, groups, obstacle_sprites, shoot):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/hero/down_dle/down_idle01.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.display_surface = pygame.display.get_surface()

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # mouvement
        self.attacking = False
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # magie
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.shoot = shoot
        self.cooldown = powers_data['fire_ball']['cooldown']

        # stats
        self.stats = {'health': 100,
                      'attack': 10, 'speed': 5}
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.is_dead = False

        # load images
        self.crosshair_img = pygame.image.load(
            '../graphics/crosshair/0.png').convert_alpha()

    def import_player_assets(self):
        character_path = '../graphics/hero/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            # mouvements
            if keys[pygame.K_z]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_q]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # boules de feu
            if pygame.mouse.get_pressed()[0]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.player_pos = self.get_pos()
                self.shoot()

            # debug death
            if keys[pygame.K_m]:
                self.health = 0

    def get_status(self):

        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        # attaques
        if self.attacking:
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

        # mort
        if self.health <= 0:
            self.is_dead = True
            self.health = 0
            # print(self.health)
            # self.kill()
            # self.visible_sprites = YSortCameraGroup()
            # try de reccrer un joueur ( marche pas)
            # self.player = Player(
            #  (2112, 1344),
            # [visible_sprites],
            #  self.obstacle_sprites,
            #  self.create_magic)

    def get_pos(self):
        return [self.rect.left, self.rect.top]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]

        # boucle sur l'index des frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # placer la bonne image pour l'animation
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        # position de la souris
        self.mouse_pos = pygame.mouse.get_pos()
