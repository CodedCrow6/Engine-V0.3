# =================================================================================================================================================================================#
#           This section adds all of the modules to syspath to ensure there are not import issues while run the engine

# =====================================!!!!!!DO NOT ALTER CONTENTS!!!!!!===========================================================================================================#

import sys
import os


def add_all_subdirectories_to_syspath(base_path):
    """
    Recursively adds all subdirectories of the base_path to sys.path.

    Args:
    base_path (str): The root directory from which to start adding subdirectories.
    """
    for root, dirs, files in os.walk(base_path):
        # Exclude unnecessary directories, e.g., '__pycache__'
        if "__pycache__" not in root:
            sys.path.append(root)


# Get the root directory of your project (the parent directory of this script)
project_root = os.path.dirname(os.path.abspath(__file__))

# Add all subdirectories of the project to sys.path
add_all_subdirectories_to_syspath(project_root)

# ==================================================================================================================================================================================#
# Beginning of main file
# ==================================================================================================================================================================================#

import pygame as pg
import pygame_gui as pyg
from core.config import RESOLUTION, DISPLAY_WIDTH, DISPLAY_HEIGHT, TARGET_FPS
from core.state_manager import StateManager
from core.input_manager import InputManager
from data_files.key_map import key_map

pg.init()
pg.font.init()


class Main:
    def __init__(self):
        # Display and Core
        self.display = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.render_surface = pg.Surface(RESOLUTION)
        self.clock = pg.time.Clock()
        self.running = True
        # Modules
        self.modules = []
        self.input_manager = InputManager(key_map)
        self.modules.append(self.input_manager)
        self.state_manager = StateManager(self, self.input_manager)
        self.modules.append(self.state_manager)
        self.ui_manager = pyg.UIManager((DISPLAY_WIDTH,DISPLAY_HEIGHT))
        # Misc
        pg.mouse.set_visible(False)
        pg.key.set_repeat(0,2)

    def get_delta_time(self):
        dt = self.clock.tick(60)/1000.0
        return dt 

    def event_handler(self):
        for event in pg.event.get():
            if (
                event.type == pg.QUIT
                or event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self.input_manager.handle_key_input(event)
                print(event)
            elif event.type == pg.KEYUP:
                self.input_manager.handle_key_input(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.input_manager.handle_mouse_input(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.input_manager.handle_mouse_input(event)

            self.ui_manager.process_events(event)

    
    def update(self):
        mouse_states = self.input_manager.get_mouse_button_states()
        for module in self.modules:
            module.update()
        self.ui_manager.update(self.get_delta_time())


    def draw(self):
        for module in self.modules:
            module.draw(self.render_surface)
        scaled_render_surface = pg.transform.scale(
            self.render_surface, (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )
        self.ui_manager.draw_ui(self.render_surface)
        self.display.blit(scaled_render_surface, (0, 0))
        
        
    def run(self):
        while self.running:
            self.display.fill("white")
            self.clock.tick(TARGET_FPS)
            self.event_handler()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    game = Main()
    game.run()
