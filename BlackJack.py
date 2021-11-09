from sys import exit
import random
from Button import Button, turn_white
from Deck import *
from Player import Player

'''
Bugs: 
- if a person except player 1 goes bankrupt the name and balance still show when first player picks his bet.

To DO:
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

Deck = deck.copy()

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
again_button = Button((0, 0, 0), (530, 260), (200, 65), 'Play again!')
place_bets = True
deal_2_cards = False
dealer_cards = False
change_bal = False
deal_cards = False
check_results = False
i = 0
j = 0

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        if len(players) == 0:
            game_active = False
        screen.fill((31, 171, 57))

        if place_bets:
            if j < len(players):
                if players[j].balance == 0:
                    players.remove(players[j])
                else:
                    if players[j].wants_bet:
                        pygame.draw.rect(screen, (31, 171, 57), (0, 0, 1200, 300), 0, -1)
                        players[j].place_bet(screen)
                    if players[j].bet != 0:
                        players[j].wants_bet = False
                    if not players[j].wants_bet:
                        j += 1
            else:
                place_bets = False
                deal_2_cards = True

        for player in players:
            player.show_name(screen)
            if not place_bets:
                player.show_cards(screen)
                player.display_score(screen)

        if not place_bets:
            player0.show_cards(screen)
            player0.display_score(screen)

        if deal_2_cards:
            for player in players:
                if player.cards is None:
                    player.cards = []
                while len(player.cards) < 2:
                    random_card = random.choice(Deck)
                    Deck.remove(random_card)
                    player.add_card(random_card)
            if player0.cards is None:
                player0.cards = []
            while len(player0.cards) < 1:
                random_card = random.choice(Deck)
                Deck.remove(random_card)
                player0.add_card(random_card)
            for player in players:
                player.wants_card = True
            deal_2_cards = False
            deal_cards = True

        if deal_cards:
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
                                    random_card = random.choice(Deck)
                                    Deck.remove(random_card)
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
                random_card = random.choice(Deck)
                Deck.remove(random_card)
                player0.add_card(random_card)
            if player0.value_count() == 0:
                pass
            else:
                while 0 < player0.value_count() < 17:
                    random_card = random.choice(Deck)
                    Deck.remove(random_card)
                    player0.add_card(random_card)
            deal_cards = False
            dealer_cards = False
            change_bal = True
            check_results = True

        if change_bal:
            dealer_score = player0.value_count()
            for player in players:
                player.adjust_balance(dealer_score)
            change_bal = False

        if check_results:
            dealer_score = player0.value_count()
            pygame.draw.rect(screen, (31, 171, 57), (0, 360, 1200, 25), 0)
            for player in players:
                player.display_results(screen, dealer_score)

            again_button.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if again_button.collides(pos):
                        deal_2_cards = False
                        deal_cards = False
                        check_results = False
                        place_bets = True
                        i = 0
                        j = 0
                        for player in players:
                            player.cards = None
                            player.wants_bet = True
                            player.wants_card = False
                        player0.cards = None
                        Deck = deck.copy()
                turn_white(again_button, event)

    else:
        screen.fill((31, 171, 57))
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
