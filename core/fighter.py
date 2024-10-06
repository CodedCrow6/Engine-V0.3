import os 
import pygame as pg 
from data_files.characters import Attributes
from core.animator import Animator 
from core.config import RENDER_WIDTH,RENDER_HEIGHT,CHARACTERS_DIR


class Fighter:
    def __init__(self,state,level,name,pos,input_manager,opponent,is_player=False):
        self.state = state
        self.name = name 
        self.level_reference = level
        self.pos = pg.math.Vector2(pos)
        self.rect = pg.Rect(self.pos,(140,420))
        self.attacking_rect = pg.Rect((1,1),(1,1))
        self.input_manager = input_manager
        self.is_player = is_player
        self.dx,self.dy = 0, 0
        self.vel_y = 0
        self.state = 0
        self.flip = False
        self.direction = self.flip
        self.animator = Animator(self,self.name)
        self.world_rect = pg.Rect((0,0),(RENDER_WIDTH,RENDER_HEIGHT))
        self.attributes = Attributes[self.name]
        self.ki_blasts = []
        self.update_time = pg.time.get_ticks()
        self.opponent = opponent # Once implemented change this to pass the opponent object rather than the rect 
       

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
            self.state = 8
        if keys['j']:
            self.attack_rect(True,3)
            self.state = 3
        if keys['k']:
            self.attack_rect(True,4)
            self.state = 4
        if keys['t']:
            self.init_ki_blast(0)
            self.state = 5
        
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left < self.world_rect.left:
            self.rect.left = self.world_rect.left
        if self.rect.right > self.world_rect.right:
            self.rect.right = self.world_rect.right
        if self.rect.top < self.world_rect.top:
            self.rect.top = self.world_rect.top
        print(f'{self.rect.x} | {self.rect.y}')

    def attack_rect(self,active,attack_type):
        if active:
            if attack_type == 3:
                self.attacking_rect = pg.Rect((self.rect.x + self.rect.width,self.rect.y),(self.rect.width ,self.rect.height // 2))
            if attack_type == 4 and self.animator.frame_index == 2:
                self.attacking_rect = pg.Rect((self.rect.x + self.rect.width,self.rect.y + (self.rect.height // 2 )),(self.rect.width * 3 ,self.rect.height // 2))
        elif active == False and attack_type == 0:
            self.attacking_rect = pg.Rect((1,1),(1,1))
            
    def init_ki_blast(self,blast_index):
        now = pg.time.get_ticks()
        if now - self.update_time >= 500:
            if blast_index == 0 and self.animator.frame_index == 2 :
                self.ki_blasts.append(KiBlast(self.rect,self.direction,self.opponent,blast_index)) 
                self.update_time = now
    
    
    def check_state(self,key_states):
        if all(value == False for value in key_states.values()):
            self.state = 6
            self.attack_rect(False,0)

    def update(self):
        self.move()
        self.animator.update()
        if len(self.ki_blasts) >= 1:
            for ki_blast in self.ki_blasts:
                ki_blast.update()
        
    def draw(self,surface):
        #pg.draw.rect(surface,'green',self.rect)
        #pg.draw.rect(surface,'red',self.attacking_rect)
        self.animator.draw(surface)
        if len(self.ki_blasts) >= 1:
            for ki_blast in self.ki_blasts:
                ki_blast.draw(surface)

class KiBlast:
    def __init__(self, character_rect, direction, opponent, blast_index):
        """
        Initialize a KiBlast instance.

        :param character_rect: The rect of the character creating the KiBlast.
        :param direction: The direction the character is facing (1 for right, -1 for left).
        :param blast_index: The type of ki blast (denoted by an integer index).
        """
        self.blast_types = [0,1]
        self.blast_index = blast_index  # Determines the type of blast (for different sprites or behaviors)
        self.blast_type = self.blast_types[self.blast_index]
        self.assets_dir = f'{CHARACTERS_DIR}/fx - one_handed_ki_blast'
        self.speed = 30  # Speed at which the blast moves
        self.direction = direction  # The direction the blast moves (1 = right, -1 = left)
        self.opponent = opponent
        self.update_time = pg.time.get_ticks()
        self.frame_index = 0
        self.animation_cache = self.get_animation_cache()
        self.image = self.animation_cache[0]
        
        # Set the initial position of the ki blast at the right-hand side of the character's rect
        if self.blast_type == 0:
            self.rect = pg.Rect(character_rect.right + 60, character_rect.centery - 110, 20, 20)  # Spawn on the right
       
        self.active = True  # Whether the blast is still active
    
    def get_animation_cache(self):
        cache = []
        for image in os.listdir(self.assets_dir):
            img = pg.image.load(f'{self.assets_dir}/{image}').convert_alpha()
            img = pg.transform.scale(img,(128,128))
            cache.append(img)
        return cache
            
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.update_time >= 100:
            self.frame_index += 1
            self.update_time = now
        if self.frame_index >= len(self.animation_cache)-1:
            self.frame_index = 0
        self.image = self.animation_cache[self.frame_index]
            
    
    def update(self):
        """
        Update the position of the ki blast, check for collisions, and deactivate if necessary.

        :param screen_width: The width of the screen (used to check if the blast leaves the screen).
        :param screen_height: The height of the screen (used to check if the blast leaves the screen).
        :param opponent_rect: The rect of the opponent character (used to check for collisions).
        """
        # Move the ki blast in the direction it was created
        self.rect.x += self.speed 
        self.animate()
        
        # Check for collisions with the opponent
        if self.rect.colliderect(self.opponent):
            self.active = False  # Deactivate the ki blast on collision
        
        # Check if the blast leaves the screen bounds
        if self.rect.right < 0 or self.rect.left > RENDER_WIDTH or self.rect.bottom < 0 or self.rect.top > RENDER_HEIGHT:
            self.active = False  # Deactivate if it leaves the screen

    def draw(self, screen):
        """
        Draw the ki blast on the screen.

        :param screen: The surface to draw the ki blast on.
        """
        screen.blit(self.image,(self.rect))
            
        
        