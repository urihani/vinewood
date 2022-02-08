import pygame
from settings import *

class powers:
    def __init__(self,powers_name):
        self = 0
    # stats
    self.powers_name = powers_name
    powers_info = powers_data[self.powers_name]
    self.damage = powers_info['damage']
    self.attack_speed = powers_info['attack_speed']
    self.reach = powers_info['reach']
    self.reload = powers_info['reload']