import pygame as pg

class Grid:
    def __init__(self,display_size,size,input_manager):
        self.block_size = size
        self.display_size = display_size
        self.input_manager = input_manager
        self.grid_enabled = True
        self.grid = []
        self.enable_grid()


    def enable_grid(self):
        x_grid = self.display_size[0] // self.block_size
        y_grid = self.display_size[1] // self.block_size

        for x in range(x_grid):
            for y in range(y_grid):
                self.grid.append(spg.Rect((x*self.block_size,y*self.block_size),(self.block_size,self.block_size)))
        print(f'{x_grid} - {y_grid}')

    
    def update(self):
        self.handle_input()

    def handle_input(self):
        key_states = self.input_manager.get_key_states()
        if key_states[pg.K_g] and self.enable_grid:
            self.enable_grid = False
        elif key_states[pg.K_g] and self.enable_grid == False:
            self.enable_grid = True

    def draw(self,surface):
        if self.grid_enabled:
            for block in self.grid:
                pg.draw.rect(surface,'gray',block,1)

        
