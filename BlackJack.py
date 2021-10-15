from sys import exit
import random
from Button import Button
from Deck import *
from Player import Player

pygame.init()
screen = pygame.display.set_mode((1200, 600))
Clock = pygame.time.Clock()

test_font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)

Blackjack_surf = test_font_big.render('Blackjack', False, (0, 0, 0))

screen.fill((31, 171, 57))

players = []
player1 = Player('Matthias', 10000, 1)
players.append(player1)
player2 = Player('Karel', 10000, 2)
players.append(player2)
player3 = Player('Yannic', 10000, 3)
players.append(player3)
player4 = Player('Jasper', 10000, 4)
players.append(player4)
game_active = False

start_button = Button((0, 0, 0), (550, 480), (100, 65), 'Play!')
deal_2_cards = True

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        screen.fill((31, 171, 57))

        for player in players:
            player.show_name(screen)

        if deal_2_cards:
            for player in players:
                while len(player.cards) < 2:
                    random_card = random.choice(deck)
                    deck.remove(random_card)
                    player.add_card(random_card)
            deal_2_cards = False

        for player in players:
            player.show_cards(screen)

    else:
        screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600, 150)))
        start_button.draw(screen)
        screen.blit(pygame.transform.rotozoom(S1.load_image(), 10, 1), (510, 250))
        screen.blit(pygame.transform.rotozoom(H1.load_image(), -10, 1), (590, 250))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.collides(pos):
                    game_active = True
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if start_button.collides(pos):
                    start_button.color = (255, 255, 255)
                else:
                    start_button.color = (0, 0, 0)

    Clock.tick(60)
