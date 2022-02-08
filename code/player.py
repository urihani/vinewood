import math
from tkinter.messagebox import NO
from tkinter.ttk import Style
import pygame
from settings import *
from support import import_folder
from entity import Entity
from projectile import *


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_magic, shoot):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
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
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.shoot = shoot

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
        character_path = '../graphics/player/'
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

            # magie
            # if keys[pygame.K_LCTRL] and not self.attacking:
            #     self.attacking = True
            #     self.attack_time = pygame.time.get_ticks()
            #     style = list(magic_data.keys())[self.magic_index]
            #     strength = list(magic_data.values())[
            #         self.magic_index]['strength']
            #     self.create_magic(style, strength)

            if pygame.mouse.get_pressed()[0]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                # self.fired = True
                self.player_pos = self.get_pos()
                # print('Player : X=' +
                #       str(self.player_pos[0]) + ' - Y=' + str(self.player_pos[1]))
                self.shoot()
            # TODO timer sur la boule de feu

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
        if self.health == 0:
            self.is_dead = True

    def get_pos(self):
        return [self.rect.left, self.rect.top]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= FIRE_COOLDOWN:
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
        self.display_surface.blit(self.crosshair_img, self.mouse_pos)
        # print('Cursor : X=' +
        #       str(self.mouse_pos[0]) + ' - Y=' + str(self.mouse_pos[1]))
