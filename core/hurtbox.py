import pygame as pg
import numpy as np
from numba import jit

class HurtboxManager:
    def __init__(self, image_cache, animator):
        """
        Initializes the HurtboxManager with the image cache and animator reference.
        
        :param image_cache: A list of cached images (frames of the animations).
        :param animator: A reference to the Animator class instance.
        """
        self.image_cache = image_cache  # Cached images from Animator
        self.animator = animator        # Animator instance to get current state and frame
        self.current_hurtbox = ''
        self.rect = pg.Rect(1,1,1,1)

    def find_hurtbox(self):
        
        current_image = self.image_cache[self.animator.animation_state][self.animator.frame_index]
        current_image_width, current_image_height = current_image.get_width(), current_image.get_height()
        current_image_x, current_image_y = self.animator.object.rect.x, self.animator.object.rect.y 
        x, y = current_image_x -30, current_image_y - 30
        width, height = current_image_width - 500, current_image_height + 30 
        
        self.rect = pg.Rect(x, y, width, height)
        
        
    def draw(self,surface):
        pg.draw.rect(surface,'red',self.rect,1)
        