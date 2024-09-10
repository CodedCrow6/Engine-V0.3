import pygame as pg 
from core.config import STATE_DIR, RENDER_WIDTH,RENDER_HEIGHT

class LoadScreen:
    def __init__(self,state_manager,input_manager):
        self.state_manager = state_manager
        self.input_manager = input_manager 
        self.background_image = pg.image.load(f'{STATE_DIR}/load_screen/load_screen.jpg').convert_alpha()
        self.background_image = pg.transform.scale(self.background_image,(RENDER_WIDTH,RENDER_HEIGHT)).convert_alpha()


    def update(self):
        pass

    def draw(self,surface):
        surface.blit(self.background_image,(0,0))