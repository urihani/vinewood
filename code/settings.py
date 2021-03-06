# réglages
WIDTH = 1024
HEIGHT = 768
FPS = 60
TILESIZE = 64

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
UI_FONT_BIG = 42

# couleurs globales
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
UI_ROW_COLOR = '#3f3b9f'
TEXT_COLOR = '#EEEEEE'

# couleurs interface
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# player
player_data = {
    'health': 100, 'attack': 10, 'speed': 5
}

# enemis
monster_data = {
    'squid': {'health': 150, 'exp': 100, 'damage': 15, 'attack_type': 'slash', 'attack_sound': '../audio/attack/slash.wav', 'speed': 4.5, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 460},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',  'attack_sound': '../audio/attack/claw.wav', 'speed': 4.5, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 700},
    'spirit': {'health': 200, 'exp': 110, 'damage': 8, 'attack_type': 'thunder', 'attack_sound': '../audio/attack/fireball.wav', 'speed': 5, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 500},
    'bamboo': {'health': 100, 'exp': 120, 'damage': 6, 'attack_type': 'leaf_attack', 'attack_sound': '../audio/attack/slash.wav', 'speed': 4.5, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 500}, }

# powers
powers_data = {
    'fire_ball': {'damage': 30, 'cooldown': 700, 'speed': 2, 'reach': 600, 'distance': 4.5},
}
