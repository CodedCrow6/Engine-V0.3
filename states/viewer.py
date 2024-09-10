import os
import pygame as pg 
from core.config import CHARACTERS_DIR, RENDER_HEIGHT, RENDER_WIDTH, FONTS_DIR, UI_DIR
from data_files.characters import CHARACTER_NAMES
from ui.button import Button
from debugger import save_to_file

pg.init()
pg.font.init()

class Viewer:
    def __init__(self, state_manager, input_manager, assets_dir=CHARACTERS_DIR):
        self.state_manager = state_manager
        self.input_manager = input_manager
       
        self.character_names = CHARACTER_NAMES
        self.font = pg.font.Font(None, 64)
        self.current_character_name = self.character_names[2]
        # Using the sorting function to group animations by prefix
        self.assets_dir = f'{assets_dir}/{self.current_character_name}/model'
        self.animation_lists = os.listdir(f'{self.assets_dir}')
        self.animation_names = self.get_animation_names()
        self.animations = self.load_sprites()
        self.update_time = pg.time.get_ticks()
        self.frame_index = 0
        self.animation_state = 0
        self.buttons = []
        self.init_ui()
        self.image = self.animations[self.animation_state][self.frame_index]
        self.viewer_rect = pg.Rect(((RENDER_WIDTH // 2) - 100, 400), (300, 400))
        self.character_rect = self.image.get_rect(topleft=(self.viewer_rect.x + 50, self.viewer_rect.y + 50))
        self.complete = False
        self.details_surface = ''
        pg.key.set_repeat(0, 2)

    def init_ui(self):
        # Cursor
        self.cursor = pg.image.load(f'{UI_DIR}/cursor.png')
        self.cursor = pg.transform.scale(self.cursor, (64, 64))
        self.cursor_rect = self.cursor.get_rect(topleft=self.input_manager.get_mouse_pos())

    def get_animation_names(self):
        animation_names = []
        for animation_folder in os.listdir(f'{self.assets_dir}'):
            animation_names.append(str(animation_folder))
        return animation_names
        
    def load_sprites(self):
        cache = []
        for animation_folder in os.listdir(self.assets_dir):
            print(animation_folder)
            animation_list = []
            for image in os.listdir(f'{self.assets_dir}/{animation_folder}'):
                frame = pg.image.load(f'{self.assets_dir}/{animation_folder}/{image}').convert_alpha()
                animation_list.append(frame)
            cache.append(animation_list)
        return cache
                
    
    def update(self):
        # Get Mouse position and Mouse Button State
        mouse_states = self.input_manager.get_mouse_button_states()
        mouse_pos = self.input_manager.get_mouse_pos()
        # Update Cursor image position to mouse_position
        self.cursor_rect = self.cursor.get_rect(topleft=self.input_manager.get_mouse_pos())
        
        # Call looped methods
        self.handle_input(mouse_states)
        self.animate()
        self.render_details()
        
    def handle_input(self, mouse_state):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.change_state(0)
        elif keys[pg.K_d]:
            self.change_state(1)
            
    def render_details(self):
        self.details_surface = self.font.render(f'Animation State: {self.animation_names[self.animation_state]}', True, 'black')
    
    def change_state(self,state):
        if state == 0:
            self.frame_index = 0
            self.animation_state -=1
        elif state == 1:
            self.frame_index = 0
            self.animation_state += 1
            
            
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.update_time >= 200:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.animation_state])
            self.update_time = now
        self.image = self.animations[self.animation_state][self.frame_index]

    def draw(self, surface):
        self.image = self.animations[self.animation_state][self.frame_index]
        surface.fill('gray')
        pg.draw.rect(surface, 'black', self.viewer_rect, 1)
        surface.blit(self.image, (self.viewer_rect))
        surface.blit(self.details_surface, (300, 400))
