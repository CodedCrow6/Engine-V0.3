import pygame as pg 

class Button:
    def __init__(self,pos,inactive_color,active_color,shadow_color,font,text):
        self.pos = pos
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.shadow_color = shadow_color
        self.color = self.inactive_color
        self.font = font
        self.text = text 
        self.rendering = self.font.render(self.text, True, self.color)
        if self.shadow_color != None:
            self.shadow_rendering = self.font.render(self.text,True,self.shadow_color)
        self.rect = self.rendering.get_rect(topleft=(self.pos))
        self.action = text
        self.pressed = False


    def handle_input(self,mouse_state,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = self.active_color
            if mouse_state[1]:
                self.pressed = True
        elif self.rect.collidepoint(mouse_pos):
            if mouse_state[1] == False:
                self.color = self.inactive_color
                self.pressed = False


    def update(self,mouse_state,mouse_pos):
        self.rendering = self.font.render(self.text, True, self.color)
        self.handle_input(mouse_state,mouse_pos)


    def draw(self,surface):
        surface.blit(self.rendering,self.rect)
        if self.shadow_color != None:
            surface.blit(self.shadow_rendering,(self.rect.x-3,self.rect.y-3))
       
        
