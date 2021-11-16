import pygame


def turn_white(button, event):
    if event.type == pygame.MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        if button.collides(pos):
            button.color = (255, 255, 255)
        else:
            button.color = (0, 0, 0)


def button_pressed(button, event):
    turn_white(button, event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if button.collides(pos):
            return True
        return False


class Button:
    def __init__(self, color, position, size, text=''):
        self.color = color
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.text = text

    def set_color(self, color):
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.pos_x - 2, self.pos_y - 2, self.width + 4, self.height + 4), 5)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, False, (0, 0, 0))
            window.blit(text, (
                self.pos_x + (self.width / 2 - text.get_width() / 2),
                self.pos_y + (self.height / 2 - text.get_height() / 2)))

    def collides(self, mouse):
        if self.pos_x - 10 < mouse[0] < (self.pos_x + self.width) + 10:
            if self.pos_y - 10 < mouse[1] < (self.pos_y + self.height) + 10:
                return True
        return False
