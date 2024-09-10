import pygame as pg 
from data_files.characters import Attributes
from core.animator import Animator 
from core.config import RENDER_WIDTH,RENDER_HEIGHT 


class Fighter:
    def __init__(self,state,level,name,pos,input_manager,is_player=False):
        self.state = state
        self.name = name 
        self.level_reference = level
        self.pos = pg.math.Vector2(pos)
        self.rect = pg.Rect(self.pos,(140,420))
        self.input_manager = input_manager
        self.is_player = is_player
        self.dx,self.dy = 0, 0
        self.vel_y = 0
        self.state = 0
        self.direction = 0
        self.flip = False
        self.animator = Animator(self,self.name)
        self.world_rect = pg.Rect((0,0),(RENDER_WIDTH,RENDER_HEIGHT))
        self.attributes = Attributes[self.name]
       

    def move(self):
        keys = self.input_manager.get_key_states()
        self.dx,self.dy = 0, 0
        
        self.check_state(keys)
        
        if keys['d']:
            self.dx += self.attributes['velocity']
            self.state = 2
        if keys['a']:
            self.dx -= self.attributes['velocity']
            self.state = 1
        if keys['s']:
            self.dy += self.attributes['velocity']
        if keys['w']:
            self.dy -= self.attributes['velocity']
            self.state = 8s
        
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left < self.world_rect.left:
            self.rect.left = self.world_rect.left
        if self.rect.right > self.world_rect.right:
            self.rect.right = self.world_rect.right
        if self.rect.top < self.world_rect.top:
            self.rect.top = self.world_rect.top
        print(f'{self.rect.x} | {self.rect.y}')

    
    def check_state(self,key_states):
        if all(value == False for value in key_states.values()):
            self.state = 6

    def update(self):
        self.move()

        self.animator.update()
        
    def draw(self,surface):
        pg.draw.rect(surface,'green',self.rect)
        self.animator.draw(surface)
        