import pygame as pg 
from core.config import LEVELS_DIR, RENDER_WIDTH, RENDER_HEIGHT

class Level:
    def __init__(self,state,data):
        self.data = data 
        self.background_image = pg.image.load(f'{LEVELS_DIR}/{self.data}').convert_alpha()
        self.background_image = pg.transform.scale(self.background_image,(RENDER_WIDTH,RENDER_HEIGHT)).convert_alpha()
        self.rect = self.background_image.get_rect(topleft=(0,0))
        
        ## Unimplemented animator and Player amd Opponent objects

    def update(self):
        pass

    def draw(self,surface):
        surface.blit(self.background_image,self.rect)