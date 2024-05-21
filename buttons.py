import pygame

pygame.init()

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = pygame.font.Font("fonts/Roboto-Black.ttf", 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            text_surface = self.font.render(self.text, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
            screen.blit(text_surface, text_rect)
    
    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
    

button1 = Button(400, 400, 200, 50, (0,0,255), 'Play again')
restart_button = Button(0, 0, 200, 50, (0, 255, 0), 'Restart')