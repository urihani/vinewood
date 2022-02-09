from asyncio.windows_events import NULL
import pygame
from settings import *


class UI:
    def __init__(self, count_monsters):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font_big = pygame.font.Font(UI_FONT, UI_FONT_BIG)
        self.count_monsters = count_monsters

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        self.clock = pygame.time.Clock()

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_count_monsters(self):
        bg_rect = pygame.Rect(550, 10, 250, 50)
        self.nb_enemies = self.count_monsters()
        #myfont = pygame.font.SysFont('Comic Sans MS', 15)
        textsurface = self.font.render(
            f"Nombre d'ennemis restants : {self.nb_enemies}", False, (0, 0, 0,))
        count_monsters_rect = textsurface.get_rect()
        #pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        self.display_surface.blit(textsurface, bg_rect)
        print(self.nb_enemies)

    def show_cauldron_menu(self):
        # print('show menu')
        bg_rect = pygame.Rect(350, 20, 350, 730)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # dash
        self.dash_rect = self.display_row(
            '../graphics/power_ups/dash.png', 355, 25)
        # fire_rate
        self.fire_rate_rect = self.display_row(
            '../graphics/power_ups/cadence.png', 355, 75)
        # damage
        self.damage_rect = self.display_row(
            '../graphics/power_ups/degats.png', 355, 125)
        # reach
        self.reach_rect = self.display_row(
            '../graphics/power_ups/portee.png', 355, 175)
        # speed
        self.speed_rect = self.display_row(
            '../graphics/power_ups/vitesse.png', 355, 225)
        # health
        self.health_rect = self.display_row(
            '../graphics/power_ups/sante.png', 355, 275)

    def display_row(self, path, x, y):
        dash_img = pygame.image.load(
            path).convert_alpha()
        rect = dash_img.get_rect(topleft=(x, y))
        self.display_surface.blit(dash_img, rect)
        return rect

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = pygame.image.load(
            '../graphics/powers/simple_fire/0.png').convert_alpha()
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def handle_event(self, event):
        # print(hasattr(self, 'cauldron_menu_visible')
        #       and self.cauldron_menu_visible)
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'dash_rect'):
            # dash
            if self.dash_rect.collidepoint(event.pos):
                print('dash - ok')
            # fire_rate
            if self.fire_rate_rect.collidepoint(event.pos):
                print('fire_rate - ok')
            # damage
            if self.damage_rect.collidepoint(event.pos):
                print('damage - ok')
            # reach
            if self.reach_rect.collidepoint(event.pos):
                print('reach - ok')
            # speed
            if self.speed_rect.collidepoint(event.pos):
                print('speed - ok')
            # health
            if self.health_rect.collidepoint(event.pos):
                print('health - ok')

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        self.show_count_monsters()
