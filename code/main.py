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

        self.level = Level()
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
        self.resume_surface = pygame.image.load(
            '../graphics/menu_pause/resume.png').convert_alpha()

        # souris menu
        self.crosshair_img = pygame.image.load(
            '../graphics/crosshair/0.png').convert_alpha()


    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.display_surface.blit(self.crosshair_img, self.mouse_pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            if self.game_pause == False and self.credit == False:
                self.level.run()

            # souris
            self.mouse_pos = pygame.mouse.get_pos()
            self.display_surface.blit(self.crosshair_img, self.mouse_pos)
            self.update()
            self.game_pause_input_check()
            pygame.display.update()
            if self.game_pause or self.credit:
                self.clock.tick(0)
                # faire disparaitre le curseur
                pygame.mouse.set_cursor()
            else:
                self.clock.tick(FPS)
                # faire disparaitre le curseur
                pygame.mouse.set_cursor(
                    (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
            self.i += 1
            print(self.is_pressed)
            print(self.i)

    def game_pause_input_check(self):
        keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.display_surface.blit(self.crosshair_img, self.mouse_pos)
        if (keys[pygame.K_ESCAPE] and self.is_pressed == False and self.credit == False ) or (self.resume == True and self.is_pressed == False and self.credit == False):
            
            self.is_pressed = True
            #self.is_waiting = False
            self.resume = False
            if self.game_pause:
                self.game_pause = False
                time.sleep(0.1)
                self.is_pressed = False
            else:
                self.game_pause = True
        if self.game_pause:
            self.clock.tick(0)
            self.display_surface.fill(((64, 64, 64)))

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

            #if not self.is_waiting:
            #self.dernierTemps = time.time()
                #self.is_waiting = True
            #while time.time() < self.dernierTemps + 0.1:
            time.sleep(0.1)
            self.is_pressed = keys[pygame.K_ESCAPE]
                #self.is_waiting = False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.resume_rect.collidepoint(event.pos):
                        self.resume = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.credit_rect.collidepoint(event.pos):
                        self.credit = True

        if self.credit:
            self.clock.tick(0)
            self.display_surface.fill(((64, 64, 64)))
            self.retour_surf = pygame.image.load('../graphics/menu_pause/retour.png').convert_alpha()
            self.retour_rect = self.retour_surf.get_rect(topleft=(0, 0))
            self.display_surface.blit(self.retour_surf, self.retour_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.retour_rect.collidepoint(event.pos):
                        self.credit = False
        

if __name__ == '__main__':
    game = Game()
    game.run()
