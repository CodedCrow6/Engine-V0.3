import pygame as pg 
from config import LEVELS_DIR
from core.level import Level
from core.fighter import Fighter

class Battle:
    def __init__(self,state_manager,input_manager,persistancy):
        self.state_manager = state_manager
        self.input_manager = input_manager
        self.level_data = persistancy[2]
        self.level = Level(self, r'C:\Users\CDE.RG\Documents\github-repos\engine_v0.3\assets\graphics\levels\Land-of-the-Kais.png')
        self.level_rect = self.level.rect
        self.opponent = persistancy[1]
        self.player = Fighter(self,self.level,persistancy[0],(100,300),self.input_manager,pg.Rect((900,300),(100,300)),True)
        
       
        self.complete = False

    def update(self):
        self.level.update()
        self.player.update()

    def draw(self,surface):
        self.level.draw(surface)
        self.player.draw(surface)