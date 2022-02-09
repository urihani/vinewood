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

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

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

    def show_cauldron_menu(self):
        bg_rect = pygame.Rect(350, 20, 350, 730)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # dash
        dash_rect = self.display_row('../graphics/power_ups/dash.png', 355, 25)
        # fire_rate
        fire_rate_rect = self.display_row(
            '../graphics/power_ups/cadence.png', 355, 75)
        # damage
        damage_rect = self.display_row(
            '../graphics/power_ups/degats.png', 355, 125)
        # reach
        reach_rect = self.display_row(
            '../graphics/power_ups/portee.png', 355, 175)
        # speed
        speed_rect = self.display_row(
            '../graphics/power_ups/vitesse.png', 355, 225)
        # health
        health_rect = self.display_row(
            '../graphics/power_ups/sante.png', 355, 275)

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # dash
                if dash_rect.collidepoint(event.pos):
                    print('dash - ok')
                # fire_rate
                if fire_rate_rect.collidepoint(event.pos):
                    print('fire_rate - ok')
                # damage
                if damage_rect.collidepoint(event.pos):
                    print('damage - ok')
                # reach
                if reach_rect.collidepoint(event.pos):
                    print('reach - ok')
                # speed
                if speed_rect.collidepoint(event.pos):
                    print('speed - ok')
                # health
                if health_rect.collidepoint(event.pos):
                    print('health - ok')

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
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.magic_overlay(player.magic_index, not player.can_switch_magic)
