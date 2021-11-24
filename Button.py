import pygame
from AudioPlay import playsound
from sys import exit


def exit_pygame(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()


def turn_white(button, event):
    if event.type == pygame.MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        if button.collides(pos):
            button.color = (255, 255, 255)
        else:
            button.color = (0, 0, 0)


def button_pressed(button, event):
    turn_white(button, event)
    exit_pygame(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if button.collides(pos):
            playsound("Sounds/ButtonClick.wav")
            return True
        return False


class Button:
    def __init__(self, color, position, size, text='', font=None):
        self.color = color
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.text = text
        self.font = font

    def set_color(self, color):
        self.color = color

    def draw(self, window):
        if self.font is None:
            font = pygame.font.SysFont('comicsans', 40)
            edge = 5
        else:
            font = pygame.font.SysFont('comicsans', 15)
            edge = 2
        pygame.draw.rect(window, self.color, (self.pos_x - 2, self.pos_y - 2, self.width + 4, self.height + 4), edge)
        if self.text != '':
            text = font.render(self.text, False, (0, 0, 0))
            window.blit(text, (
                self.pos_x + (self.width / 2 - text.get_width() / 2),
                self.pos_y + (self.height / 2 - text.get_height() / 2)))

    def collides(self, mouse):
        if self.pos_x - 10 < mouse[0] < (self.pos_x + self.width) + 10:
            if self.pos_y - 10 < mouse[1] < (self.pos_y + self.height) + 10:
                return True
        return False
