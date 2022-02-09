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


class Level:
    def __init__(self):
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

        # sprites (setup)
        self.create_map()

        # UI
        self.ui = UI()

        # boules de feu
        # animation boule de feu
        self.fire_sprites = import_folder('../graphics/powers/simple_fire/')
        self.fire_group = pygame.sprite.Group()
        self.fired = False

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

        Chaudron((2170, 300), [self.visible_sprites,
                 self.obstacle_sprites], self.obstacle_sprites)

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
                                    [self.visible_sprites],
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

    def shoot(self):
        x_dist = self.mouse_pos[0] - (1024 / 2)
        y_dist = self.mouse_pos[1] - (768 / 2)
        self.angle = math.atan2(-y_dist, x_dist)

        fire_ball = Projectile([self.visible_sprites,
                                self.attackable_sprites],
                               self.fire_sprites,
                               ((self.player.rect.x+47)),
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
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.shoot, self.player_death, self.respawn)
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
            if pygame.sprite.spritecollide(obstacle, self.fire_group, True):
                print("Need to train your aim bro")

    def run(self):
        # met à jour et dessine les sprites
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.fire_group.update()
        self.fire_group.draw(self.display_surface)
        self.visible_sprites.enemy_update(self.player, self.fire_group)
        self.ui.display(self.player)
        # player status
        self.player_dead = self.player.is_dead

        # position de la souris
        self.mouse_pos = pygame.mouse.get_pos()

        # vérification des colisions entre bullets et mobs /!\ DÉ-COMMENTEZ LORSQUE LES HITBOX DES OBSTACLES SERONT RÉDUITES
        # self.check_collide_obstacles()


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
