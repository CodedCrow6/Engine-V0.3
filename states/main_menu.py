import pygame as pg
from ui.button import Button
from core.config import RENDER_WIDTH, RENDER_HEIGHT, RESOLUTION 
from core.config import FONTS_DIR, UI_DIR, STATE_DIR

pg.font.init()

class MainMenu:
    def __init__(self,state_manager,input_manager):
        self.state_manager = state_manager
        self.input_manager = input_manager
        self.button_font = pg.font.Font(f'{FONTS_DIR}/GraveDigger.ttf',96)
        self.title_font = pg.font.Font(f'{FONTS_DIR}/Saiyan-Sans Right.ttf',256)
        self.buttons = []
        self.render_surfaces = []
        self.cursor = ''
        self.init_ui()
        self.background_image = pg.image.load(f'{STATE_DIR}/main_menu/main_menu_3.jpg').convert_alpha()
        self.background_image = pg.transform.scale(self.background_image,(RESOLUTION)).convert_alpha()
        self.background_width, self.background_height = self.background_image.get_width(),self.background_image.get_height()
        self.complete = False

    def init_ui(self):
        # Menu Buttons
        buttons = ['Local','Online','Settings','Quit']
        button_start_pos = [120,400]
        
        for index in range(len(buttons)):
            btn = Button((button_start_pos[0],button_start_pos[1] + (index *80)), 'white', 'orange', 'black', self.button_font, buttons[index])
            self.buttons.append(btn)
        
        # Title Text Layers
        self.title_text = self.title_font.render("Xtreme Fighter",True,'dark gray')
        self.title_text_shadow = self.title_font.render("Xtreme Fighter", True,'black')
        self.title_text_layer_2 = self.title_font.render("Xtreme Fighter", True, 'white')
        self.title_text_layer_3 = self.title_font.render("Xtreme Fighter", True, 'black')
        self.render_surfaces.append(self.title_text)
        self.render_surfaces.append(self.title_text_shadow)
        self.render_surfaces.append(self.title_text_layer_2)
        self.render_surfaces.append(self.title_text_layer_3)
        
        # Cursor
        self.cursor = pg.image.load(f'{UI_DIR}/cursor.png').convert_alpha()
        self.cursor = pg.transform.scale(self.cursor,(64,64))
        self.cursor_rect = self.cursor.get_rect(topleft=(self.input_manager.get_mouse_pos()))

    def handle_transition(self):
        # Check if menu buttons have been activated and transition state 
        for button in self.buttons:
            if button.action == 'Local' and button.pressed:
                self.complete = True
                print(f'Menu State completed!')

    def update(self):
        # populate mouse related variables
        mouse_pos = self.input_manager.get_mouse_pos()
        mouse_state = self.input_manager.get_mouse_button_states()

        # Update buttons 
        for button in self.buttons:
            button.update(mouse_state,mouse_pos)
        
        # Set cursor image to cursor position
        self.cursor_rect.x = mouse_pos[0]- 30
        self.cursor_rect.y = mouse_pos[1] -30

        # Check for state transition 
        self.handle_transition()

    def draw(self,surface):
        # Draw background image to screen 
        surface.blit(self.background_image,(RENDER_WIDTH//2-self.background_width//2,0))
        
        # Draw menu buttons to screen 
        for button in self.buttons:
            button.draw(surface)
        # Draw Title text to screen - unimplementated at this stage
        #offset = 5
        #for index, surf in enumerate(self.render_surfaces):
            #ssurface.blit(surf,(120+(index*offset),30))
        
        # Draw cursor image to cursor position on screen
        surface.blit(self.cursor,self.cursor_rect)

        