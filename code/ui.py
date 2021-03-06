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

        self.is_speed = False

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
        self.nb_enemies = self.count_monsters()
        if self.nb_enemies != 0:
            bg_rect = pygame.Rect(550, 10, 250, 50)
            textsurface = self.font.render(
                f"Nombre d'ennemis restants : {self.nb_enemies}", False, TEXT_COLOR)
            count_monsters_rect = textsurface.get_rect()
            self.display_surface.blit(textsurface, bg_rect)
        else:
            bg_rect = pygame.Rect(225, 250, 450, 50)
            textsurface = self.font_big.render(
                "Vous avez gagné !", False, TEXT_COLOR)
            text_fin_rect = textsurface.get_rect()
            self.display_surface.blit(textsurface, bg_rect)

    def show_cauldron_menu(self):
        # print('show menu')
        bg_rect = pygame.Rect(350, 20, 350, 730)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # dash
        if self.nb_enemies <= 47:
            if not self.player.can_dash:
                self.dash_rect = self.display_row(
                    '../graphics/power_ups/dash.png', 355, 25)
            else:
                self.dash_rect = self.display_row(
                    '../graphics/power_ups/dash_buy.png', 355, 25)
            
        else:
            self.display_row(
                '../graphics/power_ups/none3.png', 355, 25)
            self.player.can_dash = False

        # reach
        if self.nb_enemies <= 42:
            if not powers_data['fire_ball']['reach'] == 750 and not powers_data['fire_ball']['distance'] == 3:
                self.reach_rect = self.display_row(
                    '../graphics/power_ups/portee.png', 355, 75)
            else:
                self.reach_rect = self.display_row(
                    '../graphics/power_ups/portee_buy.png', 355, 75)
        else:
            self.display_row(
                '../graphics/power_ups/none5.png', 355, 75)

        # speed
        if self.nb_enemies <= 36:
            if not self.is_speed:
                self.speed_rect = self.display_row(
                    '../graphics/power_ups/vitesse.png', 355, 125)
            else:
                self.speed_rect = self.display_row(
                    '../graphics/power_ups/vitesse_buy.png', 355, 125)
        else:
            self.display_row(
                '../graphics/power_ups/none6.png', 355, 125)

        # health
        if self.nb_enemies <= 28:
            if not self.player.health == 150:
                self.health_rect = self.display_row(
                 '../graphics/power_ups/sante.png', 355, 175)
            else:
                self.health_rect = self.display_row(
                 '../graphics/power_ups/sante_buy.png', 355, 175)
        else:
            self.display_row(
                '../graphics/power_ups/none8.png', 355, 175)

        # fire_rate
        if self.nb_enemies <= 20:
            if not self.player.cooldown == 600:
                self.fire_rate_rect = self.display_row(
                    '../graphics/power_ups/cadence.png', 355, 225)
            else:
                self.fire_rate_rect = self.display_row(
                    '../graphics/power_ups/cadence_buy.png', 355, 225)
        else:
            self.display_row(
                '../graphics/power_ups/none8.png', 355, 225)

        # damage
        if self.nb_enemies <= 12:
            if not powers_data['fire_ball']['damage'] == 50:
                self.damage_rect = self.display_row(
                    '../graphics/power_ups/degats.png', 355, 275)
            else:
                self.damage_rect = self.display_row(
                    '../graphics/power_ups/degats_buy.png', 355, 275)
        else:
            self.display_row(
                '../graphics/power_ups/none8.png', 355, 275)

        # nourriture
        bg_rect = pygame.Rect(450, 355, 355, 20)
        title_surf = self.font.render('nourriture', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)

        # indication
        bg_rect = pygame.Rect(365, 400, 355, 20)
        title_surf = self.font.render(
            'Revenez ici pour vous', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)

        bg_rect = pygame.Rect(365, 420, 355, 20)
        title_surf = self.font.render(
            'nourrir et devenir', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)

        bg_rect = pygame.Rect(365, 440, 355, 20)
        title_surf = self.font.render(
            'plus fort!', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)

        bg_rect = pygame.Rect(365, 500, 355, 20)
        title_surf = self.font.render(
            'zqsd : bouger', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)
        bg_rect = pygame.Rect(365, 520, 355, 20)
        title_surf = self.font.render(
            'espace : capacité n°1', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)
        bg_rect = pygame.Rect(365, 540, 355, 20)
        title_surf = self.font.render(
            'clic gauche : tirer', False, TEXT_COLOR)
        self.display_surface.blit(title_surf, bg_rect)

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
            if self.dash_rect.collidepoint(event.pos) and self.nb_enemies <= 47:
                # print('dash - ok')
                self.player.can_dash = True
                self.show_cauldron_menu
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'reach_rect'):
            # reach
            if self.reach_rect.collidepoint(event.pos) and self.nb_enemies <= 42:
                # print('reach - ok')
                powers_data['fire_ball']['reach'] = 750
                powers_data['fire_ball']['distance'] = 3
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'speed_rect'):
            # speed
            if self.speed_rect.collidepoint(event.pos) and self.nb_enemies <= 36:
                # print('speed - ok')
                self.player.speed = 6
                self.is_speed = True
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'health_rect'):
            # health
            if self.health_rect.collidepoint(event.pos) and self.nb_enemies <= 28:
                # print('health - ok')
                self.player.health = 150
            # fire_rate
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'fire_rate_rect'):
            if self.fire_rate_rect.collidepoint(event.pos) and self.nb_enemies <= 20:
                # print('fire_rate - ok')
                self.player.cooldown = 600
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'damage_rect'):
            # damage
            if self.damage_rect.collidepoint(event.pos) and self.nb_enemies <= 12:
                # print('damage - ok')
                powers_data['fire_ball']['damage'] = 50

    def display(self, player, count_monsters):
        self.count_monsters = count_monsters
        self.player = player
        self.can_dash = self.player.can_dash
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        self.show_count_monsters()
