import pygame as pg

pg.joystick.init()

class GamePadManager:
    def __init__(self,state_manager,input_manager,logger):
        self.state_manager = state_manager
        self.input_manager = input_manager
        self.logger = logger
        self.gamepads = []

    def add_gamepad(self,objectID):
        self.gamepads.append(objectID)
        return "Added Device"

    def 