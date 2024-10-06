import pygame as pg
import time
from data_files.key_map import key_map, key_state


class InputManager:
    def __init__(self, key_map, repeat_interval=0.5):
        self.system_key_map = key_map
        self.key_map = key_map
        self.key_states = key_state
        self.key_release_delay = 0.5
        self.counter_start = pg.time.get_ticks()

        self.mouse_button_states = [
            False,
            False,
            False,
            False,
        ]  # Right button, Middle button, Left button
        
    def get_key_map(self):
        return self.key_map
    
    def get_key_states(self):
        return self.key_states

    def update(self):
        self.get_mouse_pos()

    def get_mouse_pos(self):
        return pg.mouse.get_pos()
    
    def get_mouse_button_states(self):
        return self.mouse_button_states

    def handle_mouse_input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.mouse_button_states[event.button] = True
        if event.type == pg.MOUSEBUTTONUP:
            self.mouse_button_states[event.button] = False

    def handle_key_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.unicode in self.key_map.values():
                self.key_states[event.unicode] = True
                self.counter_start = pg.time.get_ticks()
        elif event.type == pg.KEYUP:
            if event.unicode in self.key_map.values():
                if pg.time.get_ticks() - self.counter_start >= self.key_release_delay:
                    self.key_states[event.unicode] = False
                

        print(self.key_states)

    def get_key_state(self, key):
        return self.key_states.get(key, False)
       

    def draw(self, surface):
        pass
