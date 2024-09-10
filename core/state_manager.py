import pygame as pg
from states.main_menu import MainMenu
from states.selection import Selection
from states.viewer import Viewer
#from states.load_screen import LoadScreen 
from states.battle import Battle
from core.config import RESOLUTION
from ui.grid_example import GridExample
from data_files.characters import CHARACTER_NAMES
from data_files.levels import LEVEL_NAMES


class StateManager:
    def __init__(self, game, input_manager):
        self.game = game
        self.input_manager = input_manager
        self.state_index = 0
        self.states = []
        self.persistancy = [CHARACTER_NAMES[0],CHARACTER_NAMES[1],LEVEL_NAMES[0]]
        self.init_states()
        self.active_state = self.states[self.state_index]
        self.previous_state = ""
        self.next_state = 0
       
    def init_states(self):
        main_menu = MainMenu(self,self.input_manager)
        self.states.append(main_menu)
        #selection = Selection(self,self.input_manager)
        #self.states.append(selection)
        #viewer = Viewer(self,self.input_manager)
        #self.states.append(viewer)
        #load_screen = LoadScreen(self,self.input_manager)
        #self.states.append(load_screen)
        battle = Battle(self,self.input_manager,self.persistancy)
        self.states.append(battle)

    def check_state(self):
        if self.active_state.complete:
            self.previous_state = self.state_index
            self.next_state += 1
            self.set_state(self.next_state)

    def set_state(self, state_index):
        self.state_index = state_index
        self.active_state = self.states[self.state_index]

    def get_state(self):
        return self.active_state

    def update(self):
        self.check_state()
        self.active_state.update()

    def draw(self, surface):
        self.active_state.draw(surface)
