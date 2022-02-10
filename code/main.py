from re import L, T
import pygame
import sys
import time
from settings import *
from level import *
from player import Player
from leveltest import *


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('VineWood')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(UI_FONT,13)
        self.font2 = pygame.font.Font(UI_FONT,25)
       
        #intro fade
        self.intro = True

        self.ui = UI()
        self.level = Level(self.ui)
        # self.level = Leveltest()

        # music/sounds
        music = pygame.mixer.music.load('../audio/blum/blum.wav')
        pygame.mixer.music.play(-1)

        # pause
        self.i = 0
        self.dernierTemps = None
        self.is_waiting = False
        self.is_pressed = False
        self.resume = False
        self.credit = False
        self.display_surface = pygame.display.get_surface()
        self.game_pause = False
        self.event = pygame.event

        # hover
        self.resume_hover = False
        self.credit_hover = False
        self.leave_hover = False

        # souris menu
        self.crosshair_img = pygame.image.load(
            '../graphics/crosshair/0.png').convert_alpha()

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.crosshair_rect = self.crosshair_img.get_rect(
            center=self.mouse_pos)
        self.display_surface.blit(self.crosshair_img, self.crosshair_rect)

    def draw_text(self, text, x, y):
        text_surf = self.font.render(text, False, TEXT_COLOR)
        text_rect = pygame.Rect(x, y, 768, 20)
        self.display_surface.blit(text_surf, text_rect)

    def draw_text2(self, text, x, y):
        text_surf = self.font2.render(text, False, TEXT_COLOR)
        text_rect = pygame.Rect(x, y, 768, 20)
        self.display_surface.blit(text_surf, text_rect)

    def handle_event1(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.wake_rect.collidepoint(event.pos):
                self.intro = False

    def handle_event2(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.resume_rect.collidepoint(event.pos):
                self.resume = True
                self.resume_hover = False
            if self.credit_rect.collidepoint(event.pos):
                self.credit = True
                self.credit_hover = False
            if self.credit_rect.collidepoint(event.pos):
                self.leave = True
                self.leave_hover = False

        if event.type == pygame.MOUSEMOTION:
            if self.resume_rect.collidepoint(event.pos):
                self.resume_hover = True
            else:
                self.resume_hover = False

        if event.type == pygame.MOUSEMOTION:
            if self.credit_rect.collidepoint(event.pos):
                self.credit_hover = True
            else:
                self.credit_hover = False

        if event.type == pygame.MOUSEMOTION:
            if self.leave_rect.collidepoint(event.pos):
                self.leave_hover = True
            else:
                self.leave_hover = False

    def handle_event3(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.retour_rect.collidepoint(event.pos):
                self.credit = False

    def run(self):
        while True:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.ui.handle_event(self.event)
            self.screen.fill('black')
            if self.game_pause == False and self.credit == False:
                if self.intro:
                    self.display_surface.fill(((0, 0, 0)))
                    self.draw_text('Vous venez de vous réveiller, vous regardez autour de vous....',40,150)
                    self.draw_text('Une île déserte!',40,200)
                    self.draw_text('Mais un bruit effrayant vient stopper votre contemplation...',40,250)
                    self.draw_text("Des monstres! c'était sûr en fait!  ",40,300)
                    self.draw_text('La seule présence amicale dans cette nuit infernale est un vieux chaudron peu bavard...',40,350)
                    self.draw_text('Des morceaux de monstres flottent à sa surface ce qui dégage une odeur pestilentielle...',40,400)
                    self.draw_text('Vous buvez cette étrange mixture et vous vous sentez étrangement plus fort...',40,450)
                    self.draw_text('Beaucoup plus fort.',40,500)

                    self.wake_serf = pygame.image.load('../graphics/menu_pause/Wake_up.png').convert_alpha()
                    self.wake_rect = self.wake_serf.get_rect(midbottom =(800,700))
                    self.display_surface.blit(self.wake_serf, self.wake_rect)
                    self.handle_event1(self.event)
                else:
                    self.level.run()

            # souris
            self.update()
            self.game_pause_input_check()
            pygame.display.update()
            if self.game_pause or self.credit:
                #self.clock.tick(0)
                # faire disparaitre le curseur
                pygame.mouse.set_cursor()
            else:
                self.clock.tick(FPS)
                # faire disparaitre le curseur
                pygame.mouse.set_cursor(
                    (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
            self.i += 1
            # print(self.is_pressed)
            # print(self.i)

    def game_pause_input_check(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE] and self.is_pressed == False and self.credit == False) or (self.resume == True and self.is_pressed == False and self.credit == False):
            self.is_pressed = True
            #self.is_waiting = False
            self.resume = False
            if self.game_pause:
                self.game_pause = False
                self.resume_hover = False
                self.credit_hover = False
                time.sleep(0.1)
                self.is_pressed = False
            else:
                self.game_pause = True
        if self.game_pause and not self.credit:
            self.display_surface.fill(((64, 64, 64)))

            self.logo_serf = pygame.image.load(
                '../graphics/menu_pause/logo.png').convert_alpha()
            self.logo_rect = self.logo_serf.get_rect(midbottom=(512, 150))
            self.display_surface.blit(self.logo_serf, self.logo_rect)

            self.resume_surface = pygame.image.load(
                '../graphics/menu_pause/resume.png').convert_alpha()
            self.resume_rect = self.resume_surface.get_rect(
                midbottom=(512, 330))
            self.display_surface.blit(self.resume_surface, self.resume_rect)

            self.credit_surface = pygame.image.load(
                '../graphics/menu_pause/credits.png').convert_alpha()
            self.credit_rect = self.credit_surface.get_rect(
                midbottom=(512, 460))
            self.display_surface.blit(self.credit_surface, self.credit_rect)

            self.leave_surf = pygame.image.load(
                '../graphics/menu_pause/Rmenu.png').convert_alpha()
            self.leave_rect = self.leave_surf.get_rect(midbottom=(512, 590))
            self.display_surface.blit(self.leave_surf, self.leave_rect)

            # if not self.is_waiting:
            #self.dernierTemps = time.time()
            #self.is_waiting = True
            # while time.time() < self.dernierTemps + 0.1:
            time.sleep(0.1)
            self.is_pressed = keys[pygame.K_ESCAPE]
            #self.is_waiting = False

            self.handle_event2(self.event)

        if self.resume_hover:
            self.resume_surface_hover = pygame.image.load(
                '../graphics/menu_pause/resume_hover.png').convert_alpha()
            self.resume_rect = self.resume_surface_hover.get_rect(
                midbottom=(512, 330))
            self.display_surface.blit(
                self.resume_surface_hover, self.resume_rect)

        if self.credit_hover:
            self.credit_surface_hover = pygame.image.load(
                '../graphics/menu_pause/credits_hover.png').convert_alpha()
            self.credit_rect = self.credit_surface_hover.get_rect(
                midbottom=(512, 460))
            self.display_surface.blit(
                self.credit_surface_hover, self.credit_rect)

        if self.leave_hover:
            self.leave_surface_hover = pygame.image.load(
                '../graphics/menu_pause/Rmenu_hover.png').convert_alpha()
            self.leave_rect = self.leave_surface_hover.get_rect(
                midbottom=(512, 590))
            self.display_surface.blit(
                self.leave_surface_hover, self.leave_rect)

        if self.credit:
            self.display_surface.fill(((64, 64, 64)))
            self.retour_surf = pygame.image.load(
                '../graphics/menu_pause/retour.png').convert_alpha()
            self.retour_rect = self.retour_surf.get_rect(topleft=(0, 0))
            self.display_surface.blit(self.retour_surf, self.retour_rect)

            self.draw_text2('Credits',440,130)
            self.draw_text('Rôles :',220,200)
            self.draw_text('Game designeurs: Julien , Loris',260,240)
            self.draw_text('Codeurs : Julien , Loris,  loic et mathis',260,280)
            self.draw_text('graphiste : mathis',260,320)
            self.draw_text(' Ingé son :mathis',260,360)
            self.draw_text('Graphisme :',220,400)
            self.draw_text('Map et ennemies: https://pixel-boy.itch.io/ninja-adventure-asset-pack',260,440)
            self.draw_text('boule de feu: https://nyknck.itch.io/pixelarteffectfx017',260,480)
            self.draw_text('Perso: https://szadiart.itch.io/rpg-main-character',260,520)
            self.draw_text('Chaudron: https://opengameart.org/content/lpc-dungeon-elements',260,560)
            self.draw_text('aliments: https://henrysoftware.itch.io/pixel-food?download',260,600)
            self.draw_text('Son :',220,640)
            self.draw_text('musique original créer avec ',260,600)


            self.handle_event3(self.event)


if __name__ == '__main__':
    game = Game()
    game.run()
