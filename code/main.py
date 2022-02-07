from re import T
import pygame
import sys
from settings import *
from level import *
from hub import *
from player import Player
from hub import *


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('VineWood')
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.hub = Hub()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

            # mécanique de téléportation
            print('dead : ' + str(self.level.player_dead))
            print('teleport : ' + str(self.hub.player_teleport))
            if self.level.player_dead:
                self.level = Hub()
            elif self.hub.player_teleport:
                self.level = Level()


if __name__ == '__main__':
    game = Game()
    game.run()
