import pygame as pg 


key_map = {
    "move_left": 'a',
    "move_right": 'd',
    "move_up": 'w',
    "move_down": 's',
    "light_punch": 'j',
    "heavy_punch": 'k',
    "light_kick": 'l',
    "heavy_kick": '0',
    "ki_charge": 'y',
    "ki_blast_one_hand": 't',
    "block": ';',
    "special_attack": 'o',
    "grab": 'p',
    "pause": '\r',  # RETURN key
    "toggle_fly": 'z'  # Random unicode value for LSHIFT
}

key_state = {
    'a': False,
    'd': False,
    'w': False,
    's': False,
    'j': False,
    'k': False,
    'l': False,
    '0': False,
    'y': False,
    't': False,
    ';': False,
    'o': False,
    'p': False,
    '\r': False,
    'z': False
}


attack_types = {
    "light_punch": pg.K_j,
    "heavy_punch": pg.K_k,
    "light_kick": pg.K_l,
    "heavy_kick": pg.K_0,
    "block": pg.K_SEMICOLON,
    "special_attack": pg.K_o,
    "grab": pg.K_p
}

