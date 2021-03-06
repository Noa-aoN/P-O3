import pygame
from AudioPlay import playsound
from sys import exit
from Style import BLACK, WHITE, GREEN


def exit_pygame(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()


class Button:
    def __init__(self, color, position, size, text='', font=None, bg_color=(114, 200, 114)):
        self.color = color
        self.bg_color = bg_color
        self.font_color = (0, 0, 0)
        self.pos_x, self.pos_y = position
        self.width, self.height = size
        self.text = text
        self.font = font

    def set_color(self, color):
        self.color = color
        self.font_color = color

    def draw(self, window):
        w = self.width
        h = self.height
        x = self.pos_x
        y = self.pos_y
        if self.font is None:
            font = pygame.font.SysFont('comicsans', 40)
            edge = 5
        else:
            font = pygame.font.SysFont('comicsans', 15)
            edge = 3
        pygame.draw.rect(window, self.color, (x - 2, y - 2, w + 4, h+ 4), edge)
        if self.bg_color:
            pygame.draw.rect(window, self.bg_color, (x - 2, y - 2, w + 2, h + 2), 0)

        if self.text != '':
            text = font.render(self.text, False, self.font_color)
            window.blit(text, (x + (w / 2 - text.get_width() / 2), y + (h / 2 - text.get_height() / 2)))

    def collides(self, mouse):
        if self.pos_x - 10 < mouse[0] < (self.pos_x + self.width) + 10:
            if self.pos_y - 10 < mouse[1] < (self.pos_y + self.height) + 10:
                return True
        return False

    def turn_white(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if self.collides(pos):
                self.set_color(WHITE)
            else:
                self.set_color(BLACK)

    def button_pressed(self, event):
        self.turn_white(event)
        exit_pygame(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.collides(pos):
                playsound("Sounds/ButtonClick.wav")
                return True
            return False
