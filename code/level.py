import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from ui import UI
from enemy import Enemy


class Level:
    def __init__(self):
        # obtenir la surface d'affichage
        self.display_surface = pygame.display.get_surface()

        # groupes de sprites (setup)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprites d'attaque
        self.current_attack = None

        # sprites (setup)
        self.create_map()

        # UI
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/Grass'),
            'objects': import_folder('../graphics/objects')
        }

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
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'grass', random_grass_image)

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
                                    self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites], self.obstacle_sprites)

    def create_magic(self, style, strength):
        print(style)
        print(strength)

    def run(self):
        # met à jour et dessine les sprites
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)


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

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites()
                         if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
