import os
import re
import pygame as pg
from core.config import CHARACTERS_DIR
from tools.utils import resize_images, resize_to_size
from core.hurtbox import HurtboxManager
from data_files.characters import Attributes

class Animator:
    def __init__(self, obj, obj_name, resize: bool):
        # Core
        self.object = obj
        self.object_name = obj_name
        self.resize = resize
        self.assets_dir = f'{CHARACTERS_DIR}/{self.object_name}'
        # Animation 
        self.nested_animation_folders = [6]
        self.animation_offsets = Attributes[self.object_name]['animation_offset']
        self.non_looped_animations = Attributes[self.object_name]['looped_animations']
        self.palindrome_animations = Attributes[self.object_name]['palindrome_animations'] 
        self.animation_cache = self.cache_animations()
        self.animation_steps = self.get_animation_steps()
        self.animation_speed = Attributes[self.object_name]['animation_speeds']
        self.animation_loop_counter = 0
        self.frame_index = 0
        self.animation_state = 0
        self.update_time = pg.time.get_ticks()
        self.aura_timer = pg.time.get_ticks()
        
        self.image = self.animation_cache[self.animation_state][self.frame_index]
        self.image_layer_2 = pg.Surface((self.image.width, self.image.height))
        self.animation_rect = self.image.get_rect(topleft=(self.object.rect.x, self.object.rect.y))
        self.flip = self.object.flip
        self.reverse = False
        self.aura_active = False
        self.aura_animation_index = 0

    def _extract_number_from_folder(self, folder_name):
        # Extract the numeric prefix from folder name using regex
        match = re.match(r"(\d+)-", folder_name)
        if match:
            return int(match.group(1))  # Return the number as an integer
        return float('inf')  # If no numeric prefix is found, return a high number
    
    def cache_animations(self):
        """Load, scales and sets transparency color for animation frames and saves to a cache"""
        cache = []
        
        # Sort the animation folders based on the numeric prefix
        animation_folders = sorted(os.listdir(self.assets_dir), key=self._extract_number_from_folder)
        
        for index, animation_folder in enumerate(animation_folders):
            temp_list = []
            folder_path = f'{self.assets_dir}/{animation_folder}'
            for image_file in os.listdir(folder_path):
                if animation_folder == 28:
                    image_path = f'{folder_path}/{image_file}'
                    image = pg.image.load(image_path).convert_alpha()
                    image.set_colorkey('black')
                    temp_list.append(image)
                else:
                    image_path = f'{folder_path}/{image_file}'
                    image = pg.image.load(image_path).convert_alpha()
                    temp_list.append(image)
            cache.append(temp_list)
        
        if self.resize:
            new_cache = resize_to_size(self.assets_dir, 'anim', (270, 350))
            return new_cache
        else:
            return cache
    
    
    def get_animation_cache(self):
        """Returns a nested list of animation images"""
        return self.animation_cache
    
    
    def get_animation_steps(self):
        steps = []
        for animation in self.animation_cache:
            steps.append(len(animation))
        return steps

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.update_time >= self.animation_speed[self.animation_state]:
            self.update_time = now

            # Handle palindrome animations
            if self.animation_state in self.palindrome_animations:
                if not self.reverse:
                    self.frame_index += 1
                    if self.frame_index >= self.animation_steps[self.animation_state] - 1:
                        self.reverse = True  # Start reversing
                else:
                    self.frame_index -= 1
                    if self.frame_index <= 0:
                        self.reverse = False  # Start moving forward again
            else:
                # Handle normal animations
                self.frame_index += 1

            if self.animation_state == 18:
                self.aura_active = True
            else:
                self.aura_active = False

            # Ensure frame_index stays within bounds
            if self.frame_index >= self.animation_steps[self.animation_state]:
                if self.animation_state in self.non_looped_animations:
                    # Stop at last frame for non-looping animations
                    self.frame_index = self.animation_steps[self.animation_state] - 1
                else:
                    # Loop animations
                    self.frame_index = 0
                    self.animation_loop_counter += 1

        # Safety check to ensure frame index is in bounds
        if self.frame_index < len(self.animation_cache[self.animation_state]):
            self.image = self.animation_cache[self.animation_state][self.frame_index]
        else:
            print(f"Warning: frame_index {self.frame_index} out of range for animation_state {self.animation_state}")
            self.frame_index = 0  # Reset to prevent crash
            self.image = self.animation_cache[self.animation_state][self.frame_index]

        if self.aura_active:
            if now - self.update_time >= 200:
                self.aura_animation_index += 1
                self.aura_timer = now
        self.image_layer_2 = self.animation_cache[28][self.aura_animation_index]
        self.image_layer_2.blit(self.image_layer_2,(0, 0))


    def set_state(self):
        if self.animation_state != self.object.state and self.animation_loop_counter > 0:
            self.frame_index = 0
            self.animation_state = self.object.state
            self.reverse = False  
    
    def update(self):
        self.animate()
        self.set_state()
        self.animation_rect = self.object.rect
        self.object.rect = self.image.get_rect(topleft=self.object.pos)
    
    def draw(self, surface):
        if self.aura_active:
            surface.blit(self.image_layer_2, (self.animation_rect.x, self.animation_rect.y))
        surface.blit(pg.transform.flip(self.image, self.flip, False),
                     (self.animation_rect.x + self.animation_offsets[self.animation_state][0],
                      self.animation_rect.y + self.animation_offsets[self.animation_state][1]))

        

