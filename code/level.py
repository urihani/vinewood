from os import kill
from tkinter.messagebox import NO
from turtle import pos
import pygame
import math
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from ui import UI
from enemy import Enemy
from projectile import *
from chaudron import Chaudron
from particles import AnimationPlayer


class Level:
    def __init__(self, ui):
        # obtenir la surface d'affichage
        self.display_surface = pygame.display.get_surface()

        # groupes de sprites (setup)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # sprites d'attaque
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        # sprites (setup)
        self.create_map()

        # nombre de monstre sur la map
        self.nb_monster = 0
        self.nb_monsterMax()

        # UI
        # self.ui = UI(self.count_monsters)

        self.ui = ui

        # boules de feu
        # animation boule de feu
        self.fire_sprites = import_folder('../graphics/powers/simple_fire/')
        self.fire_group = pygame.sprite.Group()
        self.fired = False

        self.is_displayed = False
        self.pressed = False
        self.press_time = None

        # particles
        self.animation_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }

        Chaudron(
            (2170, 300),
            [self.visible_sprites,
             self.obstacle_sprites,
             self.interactable_sprites],
            self.obstacle_sprites)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # positions
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        # limites du terrain
                        if style == 'boundary':
                            Tile(
                                (x, y), [self.obstacle_sprites], 'invisible')
                        # herbe
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y),
                                [self.visible_sprites,
                                 self.obstacle_sprites,
                                 self.attackable_sprites],
                                'grass',
                                random_grass_image)

                        # objets
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                          self.obstacle_sprites], 'object', surf)

                            # entities
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites,
                                     self.player_group],
                                    self.obstacle_sprites,
                                    self.shoot,
                                    self.player_death,
                                    self.respawn)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                self.enemy = Enemy(monster_name,
                                                   (x, y),
                                                   [self.visible_sprites,
                                                       self.attackable_sprites,
                                                       self.enemy_sprites],
                                                   self.obstacle_sprites)

    def nb_monsterMax(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        if style == 'entities':
                            if col == '390' or col == '391' or col == '392' or col == '393':
                                self.nb_monster += 1

    def count_monsters(self):
        nb = len(self.enemy_sprites)
        return nb

    def shoot(self):
        x_dist = self.mouse_pos[0] - (1024 / 2)
        y_dist = self.mouse_pos[1] - (768 / 2)
        self.angle = math.atan2(-y_dist, x_dist)

        fire_ball = Projectile([self.visible_sprites,
                                self.attackable_sprites],
                               self.fire_sprites,
                               ((self.player.rect.x+40)),
                               (self.player.rect.y+40),
                               self.angle)
        self.fire_group.add(fire_ball)

    def player_death(self):
        self.player.kill()

        for sprite in self.enemy_sprites:
            sprite.kill()

    def respawn(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # positions
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # entities
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites,
                                     self.player_group],
                                    self.obstacle_sprites,
                                    self.shoot,
                                    self.player_death,
                                    self.respawn)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                self.enemy = Enemy(monster_name,
                                                   (x, y),
                                                   [self.visible_sprites,
                                                       self.attackable_sprites,
                                                       self.enemy_sprites],
                                                   self.obstacle_sprites)

    def check_collide_obstacles(self):
        for obstacle in self.obstacle_sprites:
            if len(self.fire_group.sprites()) >= 1:
                for fire_ball in self.fire_group:
                    if obstacle.hitbox2.colliderect(fire_ball.hitbox):
                        if obstacle.sprite_type != 'invisible':
                            fire_ball.kill()
                        if obstacle.sprite_type == 'grass':
                            self.animation_player.create_grass_particles(
                                pos, [self.visible_sprites])
                            obstacle.kill()

    def check_collide_interactable(self):
        self.keys = pygame.key.get_pressed()

        for interactable in self.interactable_sprites:
            if pygame.sprite.spritecollide(interactable, self.player_group, False):
                self.ui.show_cauldron_menu()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.pressed:
            if current_time - self.pressed >= 4000:
                self.pressed = False

    def run(self):
        # met à jour et dessine les sprites
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.fire_group.update()
        self.fire_group.draw(self.display_surface)
        self.visible_sprites.enemy_update(self.player, self.fire_group)
        self.ui.display(self.player, self.count_monsters)
        # player status
        self.player_dead = self.player.is_dead

        for sp in self.interactable_sprites:
            print(sp)

        for pl in self.player_group:
            print(pl)

        print("confirm")
        # position de la souris
        self.mouse_pos = pygame.mouse.get_pos()

        # vérification des colisions entre bullets et mobs /!\ DÉ-COMMENTEZ LORSQUE LES HITBOX DES OBSTACLES SERONT RÉDUITES
        self.check_collide_obstacles()

        # intéraction avec le chaudron
        self.check_collide_interactable()

        self.count_monsters()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # création du sol
        self.floor_surf = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    # méthode pour ordonner les sprites
    # le joueur peut légèrement chevaucher les obstacles
    def custom_draw(self, player):

        # obtenir le décalage
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # dessiner le sol
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player, fire_group):
        enemy_sprites = [sprite for sprite in self.sprites()
                         if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, fire_group)
