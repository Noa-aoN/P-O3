import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200, 600))
Clock = pygame.time.Clock()

test_font = pygame.font.Font('Font/Roboto-Regular.ttf', 20)

screen.fill((71, 101, 77))


deck = ['1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H', '13H',
        '1R', '2R', '3R', '4R', '5R', '6R', '7R', '8R', '9R', '10R', '11R', '12R', '13R',
        '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S', '13S',
        '1K', '2K', '3K', '4K', '5K', '6K', '7K', '8K', '9K', '10K', '11K', '12K', '13K']


class Player:
    def __init__(self, name):
        self.name = name


player1 = Player('Matthias:')
player2 = Player('Bram:')
player3 = Player('Yanninck:')
Player4 = Player('Jasper:')

player1_surf = test_font.render(player1.name, False, (10, 10, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(player1_surf, player1_surf.get_rect(bottomleft=(50, 425)))

    pygame.display.update()
    Clock.tick(60)
