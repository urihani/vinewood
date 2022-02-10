import pygame
from settings import *


class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font_big = pygame.font.Font(UI_FONT, UI_FONT_BIG)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        self.clock = pygame.time.Clock()

        self.nb_temp = 28

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
        # print(self.nb_enemies)

    def show_cauldron_menu(self):
        # print('show menu')
        bg_rect = pygame.Rect(350, 20, 350, 730)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # dash
        if self.nb_temp <= 47:
            self.dash_rect = self.display_row(
                '../graphics/power_ups/dash.png', 355, 25)
        else:
            self.display_row(
                '../graphics/power_ups/none.png', 355, 25)
            self.player.can_dash = False

        # reach
        if self.nb_temp <= 42:
            self.reach_rect = self.display_row(
                '../graphics/power_ups/portee.png', 355, 75)
        else:
            self.display_row(
                '../graphics/power_ups/none.png', 355, 75)

        # speed
        if self.nb_temp <= 36:
            self.speed_rect = self.display_row(
                '../graphics/power_ups/vitesse.png', 355, 125)
        else:
            self.display_row(
                '../graphics/power_ups/none.png', 355, 125)

        # health
        if self.nb_temp <= 28:
            self.health_rect = self.display_row(
                '../graphics/power_ups/sante.png', 355, 175)
        else:
            self.display_row(
                '../graphics/power_ups/none.png', 355, 175)

        # fire_rate
        if self.nb_temp <= 20:
            self.fire_rate_rect = self.display_row(
                '../graphics/power_ups/cadence.png', 355, 225)
        else:
            self.display_row(
                '../graphics/power_ups/none.png', 355, 225)

        # damage
        if self.nb_temp <= 12:
            self.damage_rect = self.display_row(
                '../graphics/power_ups/degats.png', 355, 275)
        else:
            self.display_row(
                '../graphics/power_ups/none.png', 355, 275)

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
            if self.dash_rect.collidepoint(event.pos) and self.nb_temp <= 47:
                print('dash - ok')
                self.player.can_dash = True
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'reach_rect'):
            # reach
            if self.reach_rect.collidepoint(event.pos) and self.nb_temp <= 42:
                print('reach - ok')
                powers_data['fire_ball']['reach'] = 1200
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'speed_rect'):
            # speed
            if self.speed_rect.collidepoint(event.pos) and self.nb_temp <= 36:
                print('speed - ok')
                self.player.speed = 6
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'health_rect'):
            # health
            if self.health_rect.collidepoint(event.pos) and self.nb_temp <= 28:
                print('health - ok')
                self.player.health = 150
            # fire_rate
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'fire_rate_rect'):
            if self.fire_rate_rect.collidepoint(event.pos) and self.nb_temp <= 20:
                print('fire_rate - ok')
                self.player.cooldown = 300
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'damage_rect'):
            # damage
            if self.damage_rect.collidepoint(event.pos) and self.nb_temp <= 12:
                print('damage - ok')

    def display(self, player, count_monsters):
        self.count_monsters = count_monsters
        self.player = player
        self.can_dash = self.player.can_dash
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        self.show_count_monsters()
