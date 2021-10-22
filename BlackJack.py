from sys import exit
import random
from Button import Button, turn_white
from Deck import *
from Player import Player

'''
Bugs: 
- If dealer busts the game crashes. -->Fixed
- If last player has 21 the game crashes. --> Fixed
- If everyone stands the game can crash. -->Fixed
- If everyone busts the game can crash. -->Fixed

To DO:
- Turn hit- and stand buttons white when hovering over them. --> Done
- Restarting rounds.
- Showing who won and who lost.
- Betting on the rounds.
- Adding double down feature.
- Dealer has to check if he has Blackjack to terminate the round immediately.
- Adding delay with generating cards.
- Entering player names and amount of players.
- Entering starting balance.
- ...
'''

pygame.init()
screen = pygame.display.set_mode((1200, 600))
Clock = pygame.time.Clock()

test_font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
test_font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)

Blackjack_surf = test_font_big.render('Blackjack', False, (0, 0, 0))

screen.fill((31, 171, 57))

players = []
player0 = Player('Dealer', 0, 0)
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
yes_button = Button((0, 0, 0), (400, 250), (110, 60), 'Hit')
no_button = Button((0, 0, 0), (700, 250), (110, 60), 'Stand')
deal_2_cards = True
dealer_cards = False
i = 0

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
            while len(player0.cards) < 1:
                random_card = random.choice(deck)
                deck.remove(random_card)
                player0.add_card(random_card)
            for player in players:
                player.wants_card = True
            deal_2_cards = False

        for player in players:
            player.show_cards(screen)
            player.display_score(screen)
        player0.show_cards(screen)
        player0.display_score(screen)

        if i < len(players):
            if players[i].wants_card:
                if players[i].value_count() == 'bust':
                    players[i].wants_card = False
                if players[i].value_count() == 21:
                    i += 1
                else:
                    another_card_surf = test_font.render(players[i].name + ', do you want another card?',
                                                         False, (0, 0, 0))
                    screen.blit(another_card_surf, another_card_surf.get_rect(midbottom=(600, 200)))
                    yes_button.draw(screen)
                    no_button.draw(screen)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if yes_button.collides(pos):
                                random_card = random.choice(deck)
                                deck.remove(random_card)
                                players[i].add_card(random_card)
                                players[i].show_cards(screen)
                                players[i].display_score(screen)
                            elif no_button.collides(pos):
                                players[i].wants_card = False
                        turn_white(yes_button, event)
                        turn_white(no_button, event)
                if i >= len(players):
                    pass
                else:
                    if not players[i].wants_card:
                        i += 1
        else:
            dealer_cards = True
        if dealer_cards:
            if len(player0.cards) == 1:
                random_card = random.choice(deck)
                deck.remove(random_card)
                player0.add_card(random_card)
            if player0.value_count() == 0:
                dealer_cards = False
            else:
                while 0 < player0.value_count() < 17:
                    random_card = random.choice(deck)
                    deck.remove(random_card)
                    player0.add_card(random_card)
                dealer_cards = False

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
            turn_white(start_button, event)

    Clock.tick(60)
