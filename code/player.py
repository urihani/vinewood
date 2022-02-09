import math
import time
from tkinter.messagebox import NO
from tkinter.ttk import Style
from unittest import main
import pygame
from settings import *
from support import import_folder
from entity import Entity
from projectile import *


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, shoot, player_death, respawn):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/hero/up_idle/up_idle_01.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.display_surface = pygame.display.get_surface()

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # font
        self.test_font = pygame.font.Font('../font/Pixeltype.ttf', 50)

        # time
        self.dernierTemps = None
        self.is_waiting = False
        self.is_pressed = False
        self.resume = False
        self.credit = False

        # mouvement
        self.attacking = False
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.game_pause = False

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

        # méthodes partagées
        self.player_death = player_death
        self.respawn = respawn

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

    def game_pause(self):
        self.game_pause

    def input(self):
        keys = pygame.key.get_pressed()
        if self.game_pause == False:
            # if not self.attacking:
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
            if pygame.mouse.get_pressed()[0] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.player_pos = self.get_pos()
                self.shoot()

            # debug death
            if keys[pygame.K_m]:
                self.health = 0

        if keys[pygame.K_ESCAPE] and self.is_pressed == False or self.resume == True and self.is_pressed == False:
            self.is_pressed = True
            self.is_waiting = False
            if self.game_pause:
                self.game_pause = False
            else:
                self.game_pause = True
        if self.game_pause:
            self.display_surface.fill(((64, 64, 64)))

            self.resume_surface = pygame.image.load(
                '../graphics/menu_pause/resume.png').convert_alpha()
            self.resume_rect = self.resume_surface.get_rect(
                midbottom=(512, 330))
            self.display_surface.blit(self.resume_surface, self.resume_rect)

            self.credit_surface = pygame.image.load(
                '../graphics/menu_pause/credit.png').convert_alpha()
            self.credit_rect = self.credit_surface.get_rect(
                midbottom=(512, 460))
            self.display_surface.blit(self.credit_surface, self.credit_rect)

            self.Rmenu_surface = pygame.image.load(
                '../graphics/menu_pause/Rmenu.png').convert_alpha()
            self.Rmenu_rect = self.Rmenu_surface.get_rect(midbottom=(512, 590))
            self.display_surface.blit(self.Rmenu_surface, self.Rmenu_rect)

            if not self.is_waiting:
                self.dernierTemps = time.time()
                self.is_waiting = True
            if time.time() > self.dernierTemps + 0.1:
                self.is_pressed = False
                self.is_waiting = False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.resume_rect.collidepoint(event.pos):
                        self.resume = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.credit_rect.collidepoint(event.pos):
                        self.credit = True

        if self.credit and self.game_pause:
            self.display_surface.fill(((64, 64, 64)))

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
            self.player_death()
            self.respawn()

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
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        # position de la souris
        self.input()
        self.mouse_pos = pygame.mouse.get_pos()
        self.display_surface.blit(self.crosshair_img, self.mouse_pos)

        print(self.rect.left)
        print(self.rect.top)
