import pygame as pg
import random
from core.config import STATE_DIR, RENDER_HEIGHT, RENDER_WIDTH, UI_DIR, FONTS_DIR
from data_files.characters import CHARACTER_NAMES
from ui.button import Button

pg.font.init()

class Selection:
    def __init__(self, state_manager, input_manager):
        self.state_manager = state_manager
        self.input_manager = input_manager
        self.character_names = CHARACTER_NAMES
        self.font = pg.font.Font(f'{FONTS_DIR}/Saiyan-Sans.ttf', 64)
        self.bg_image = pg.image.load(f'{STATE_DIR}/selection/bg5.jpg')
        self.bg_image = pg.transform.scale(self.bg_image, (RENDER_WIDTH, RENDER_HEIGHT)).convert_alpha()
        self.sprite_width, self.sprite_height = 120, 120  # Resized for grid layout
        self.character_spritesheet = pg.image.load(f'{STATE_DIR}/selection/spritesheet.png').convert_alpha()
        self.cursor_image = pg.image.load(f'{UI_DIR}/cursor.png').convert_alpha()
        self.cursor_image = pg.transform.scale(self.cursor_image, (64, 64))
        self.cursor_rect = self.cursor_image.get_rect(topleft=(0, 0))

        # Initialize grid parameters for character display
        self.grid_cols = 8  # Number of columns for character grid
        self.grid_rows = 4   # Number of rows for character grid
        self.spacing_x = 15
        self.spacing_y = 15
        self.character_headshots = self.load_headshots()
        self.current_index = 0
        self.selected_character = None
        self.opponent_character = None
        self.persistancy = [self.selected_character, self.opponent_character]
        self.complete = False

        # Buttons for navigation
        self.next_button = Button((RENDER_WIDTH - 150, RENDER_HEIGHT - 150), 'white', 'orange', 'black', self.font, 'NEXT')
        self.previous_button = Button((50, RENDER_HEIGHT - 150), 'white', 'orange', 'black', self.font, 'PREVIOUS')
        self.buttons = [self.next_button, self.previous_button]

    def load_headshots(self):
        """Loads character headshots from the spritesheet for the grid layout."""
        headshots = []
        for i in range(len(self.character_names)):
            x = (i % 6) * self.sprite_width
            y = (i // 6) * self.sprite_height
            image = self.character_spritesheet.subsurface(x, y, self.sprite_width, self.sprite_height)
            headshots.append(image)
        return headshots

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))

        # Draw title at the top
        title_surf = self.font.render('SELECT CHARACTER', True, (255, 0, 0))
        surface.blit(title_surf, (RENDER_WIDTH // 2 - title_surf.get_width() // 2, 50))

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

        # Draw character grid
        start_x = (RENDER_WIDTH - (self.grid_cols * (self.sprite_width + self.spacing_x))) // 2
        start_y = (RENDER_HEIGHT // 2) - (self.grid_rows * (self.sprite_height + self.spacing_y)) // 2
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                character_index = (row * self.grid_cols + col) % len(self.character_headshots)
                headshot = self.character_headshots[character_index]
                x_pos = start_x + col * (self.sprite_width + self.spacing_x)
                y_pos = start_y + row * (self.sprite_height + self.spacing_y)
                surface.blit(headshot, (x_pos, y_pos))

                # Highlight selected character
                if character_index == self.selected_character:
                    pg.draw.rect(surface, (255, 255, 0), (x_pos, y_pos, self.sprite_width, self.sprite_height), 5)
                # Highlight hovered character
                elif headshot.get_rect(topleft=(x_pos, y_pos)).collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(surface, (255, 0, 0), headshot.get_rect(topleft=(x_pos, y_pos)), 3)

        # Draw cursor
        surface.blit(self.cursor_image, self.cursor_rect)

        # Display larger image or highlight selected character
        if self.selected_character is not None:
            enlarged_image = pg.transform.scale(self.character_headshots[self.selected_character], (self.sprite_width * 2, self.sprite_height * 2))
            surface.blit(enlarged_image, (RENDER_WIDTH - enlarged_image.get_width() - 50, 50))

    def update(self):
        mouse_pos = self.input_manager.get_mouse_pos()
        mouse_state = self.input_manager.get_mouse_button_states()

        # Update cursor position
        self.cursor_rect.topleft = (mouse_pos[0] - 30, mouse_pos[1] - 30)

        # Update button objects
        for button in self.buttons:
            button.update(mouse_state, mouse_pos)

        # Check button interactions
        self.handle_buttons(mouse_state)

        # Check character selection in the grid
        start_x = (RENDER_WIDTH - (self.grid_cols * (self.sprite_width + self.spacing_x))) // 2
        start_y = (RENDER_HEIGHT // 2) - (self.grid_rows * (self.sprite_height + self.spacing_y)) // 2

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                character_index = (row * self.grid_cols + col) % len(self.character_headshots)
                x_pos = start_x + col * (self.sprite_width + self.spacing_x)
                y_pos = start_y + row * (self.sprite_height + self.spacing_y)
                headshot_rect = self.character_headshots[character_index].get_rect(topleft=(x_pos, y_pos))
                if headshot_rect.collidepoint(mouse_pos) and mouse_state[1]:  # Mouse left-click
                    self.selected_character = character_index
                    self.opponent_character = random.choice([i for i in range(len(self.character_headshots)) if i != self.selected_character])
                    self.state_manager.persistancy.append(self.selected_character)
                    self.state_manager.persistancy.append(self.opponent_character)
                    self.state_manager.persistancy.append(0)
                    self.complete = True

    def handle_buttons(self, mouse_state):
        """Handles button actions for next and previous navigation."""
        for button in self.buttons:
            if button.pressed:
                if button.action == 'NEXT' and not mouse_state[1]:  # Trigger on mouse release
                    self.current_index = (self.current_index + 1) % len(self.character_headshots)
                    button.pressed = False  # Reset button press state
                elif button.action == "PREVIOUS" and not mouse_state[1]:  # Trigger on mouse release
                    self.current_index = (self.current_index - 1) % len(self.character_headshots)
                    button.pressed = False  # Reset button press state
