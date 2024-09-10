import pygame as pg 
from core.config import FONTS_DIR, RENDER_HEIGHT

class Slot:
    def __init__(self,pos,image,character_name):
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.font = pg.font.Font(f'{FONTS_DIR}/Saiyan-Sans Left.ttf',64)
        self.character_name = self.font.render(character_name,True,'black')

    def update(self,pressed,direction=0):
        if pressed and direction == 1:
            self.rect.x -= self.rect.width
        elif pressed and direction == 0:
            self.rect.x += self.rect.width
        else:
            pass

    def draw(self,surface):
        #pg.draw.rect(surface,'black',self.rect,1)
        surface.blit(self.image,(self.rect.x,self.rect.y))
       # surface.blit(self.character_name,(20,RENDER_HEIGHT - self.rect.height - 20))