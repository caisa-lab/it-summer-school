import pygame
import pygame.gfxdraw

buttons = pygame.sprite.Group()

class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size, command,
        colors="white on blue",
        hover_colors="red on green", borderc=(255,255,255), padding = 10):
        # the hover_colors attribute needs to be fixed
        super().__init__()
        self.text = text
        self.command = command
        self.padding = padding
        # --- colors ---
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        if hover_colors == "red on green":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors
        self.borderc = borderc 
        # font
        self.font = pygame.font.SysFont("Arial", size)
        self.render()
        _, _, self.w , self.h = self.text_render.get_rect()
        self.x, self.y, _, _ = position
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.position = position
        self.pressed = 1
        buttons.add(self)
 
    def render(self):
        self.text_render = self.font.render(self.text, 1, self.fg)
        self.image = self.text_render
        
    def update(self, win):
        self.fg, self.bg = self.colors.split(" on ")
        self.draw_button(win)
        self.hover()
        self.click()

    def draw_button(self, win):
        ''' a linear border '''
        pygame.draw.rect(win, self.bg, (self.x - self.padding, self.y - self.padding, self.w + (2*self.padding), self.h + (2 * self.padding)))
        pygame.gfxdraw.rectangle(win, (self.x - self.padding, self.y - self.padding, self.w + (2*self.padding), self.h + (2 * self.padding)), self.borderc)
 
    def hover(self):
        ''' checks if the mouse is over the button and changes the color if it is true '''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # you can change the colors when the pointer is on the button if you want
            self.colors = self.hover_colors
        else:
            self.colors = self.original_colors
            
        self.render()
 
    def click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command()
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1