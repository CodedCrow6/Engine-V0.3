import os 
import pygame as pg 
from core.config import CHARACTERS_DIR
from tools.image_sorter import move_files_to_groups

class Animator:
    def __init__(self,obj,obj_name):
        self.object = obj
        self.object_name = obj_name
        self.assets_dir = f'{CHARACTERS_DIR}/{self.object_name}'
        self.animation_offset = (-250,-150)
        #self.sort_animation_folders(self.assets_dir)
        self.animation_cache = self.cache_animations()
        self.animation_steps = self.get_animation_steps()
        self.animation_speed = self.get_animation_speeds()
        self.non_looped_animations = [1,2,8]
        self.frame_index = 0 
        self.animation_state = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animation_cache[self.animation_state][self.frame_index]
        self.animation_rect = self.image.get_rect(topleft=(self.object.rect.x,self.object.rect.y))
        self.flip = self.object.flip
        
    def sort_animation_folders(self,directory):
        move_files_to_groups(directory)
        
    def cache_animations(self):
        cache = []
        for animation_folder in os.listdir(self.assets_dir):
            temp_list = []
            for image_file in os.listdir(f'{self.assets_dir}/{animation_folder}'):
                print(image_file)
                image = pg.image.load(f'{self.assets_dir}/{animation_folder}/{image_file}').convert_alpha()
                #image = pg.transform.scale(image,(200,200))
                temp_list.append(image)
            cache.append(temp_list)
        return cache
    
    def get_animation_steps(self):
        steps = []
        for animation in self.animation_cache:
            steps.append(len(animation))
        return steps
    
    def get_animation_speeds(self):
        speed = []
        for step in self.animation_steps:
            speed.append(250)
        return speed
            
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.update_time >= self.animation_speed[self.animation_state]:
            self.frame_index += 1
            self.update_time = now

        # Handle non-looping animations
        if self.animation_state in self.non_looped_animations:
            if self.frame_index >= self.animation_steps[self.animation_state] - 1:
                self.frame_index = self.animation_steps[self.animation_state] - 1  # Stop at last frame
        else:
            # Loop animations
            if self.frame_index >= self.animation_steps[self.animation_state] - 1:
                self.frame_index = 0

        self.image = self.animation_cache[self.animation_state][self.frame_index]

        
    def update(self):
        self.animate()
        self.animation_state = self.object.state
        self.animation_rect = self.object.rect
        
    def draw(self,surface):
        pg.draw.rect(surface,'white',self.animation_rect)
        surface.blit(pg.transform.flip(self.image,self.flip,False),(self.animation_rect.x + self.animation_offset[0],self.animation_rect.y + self.animation_offset[1]))
        
        
        