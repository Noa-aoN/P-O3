from sys import exit
from Button import Button, button_pressed, exit_pygame
from Deck import load_deck, get_random_card, load_random_deck
from Player import Player
from AudioPlay import playsound
from time import sleep
import pygame

'''
Bugs: 

To DO:
- Adding delay with generating cards.
- Entering player names and amount of players.
- Entering starting balance.
- ...
'''


def blackjack(screen, clock):
    test_font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
    test_font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)
    test_font_small = pygame.font.Font('Font/Roboto-Regular.ttf', 11)

    Blackjack_surf = test_font_big.render('Blackjack', False, (0, 0, 0))
    f = open('blackjackrules.txt', 'r')
    content = f.read()

    deck = load_random_deck()

    player0 = Player('Dealer', 0, 0)
    names = ['Matthias', 'Karel', 'Yannic', 'Jasper']
    players = [player0] + [Player(name, 10000, i + 1) for i, name in enumerate(names)]
    game_active = False

    start_button = Button((0, 0, 0), (550, 480), (100, 65), 'Play!')
    yes_button = Button((0, 0, 0), (330, 250), (110, 60), 'Hit')
    no_button = Button((0, 0, 0), (770, 250), (110, 60), 'Stand')
    double_button = Button((0, 0, 0), (475, 250), (250, 60), 'Double Down')
    again_button = Button((0, 0, 0), (530, 260), (200, 65), 'Play again!')
    exit_button = Button((0, 0, 0), (1140, 20), (40, 20), 'Exit', 'small')
    rules_button = Button((0, 0, 0), (1140, 560), (40, 20), 'Rules', 'small')

    place_bets = True
    deal_2_cards = False
    dealer_cards = False
    change_bal = False
    deal_cards = False
    check_results = False
    rules = False
    i = 0
    j = 0

    playing_bj = True

    while playing_bj:

        pygame.display.update()

        if game_active:

            if len(players) == 0:
                game_active = False
            screen.fill((31, 171, 57))

            if place_bets:
                if j < len(players):
                    for player in players:
                        if player.balance == 0:
                            players.remove(player)
                    if players[j].wants_bet:
                        pygame.draw.rect(screen, (31, 171, 57), (0, 0, 1200, 300), 0, -1)
                        status = players[j].place_bet(screen, exit_button)
                        if status == 'exit':
                            return 'Done'
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
                    player.display_score_bj(screen)

            if not place_bets and not check_results:
                player0.show_cards(screen)
                player0.display_score_bj(screen)

            if deal_2_cards:
                for player in players:
                    if player.cards is None:
                        player.cards = []
                    while len(player.cards) < 2:
                        random_card, deck = get_random_card(deck)
                        player.add_card(random_card)
                        player.show_cards(screen)
                        player.display_score_bj(screen)
                        pygame.display.update()
                        sleep(1)
                        random_card, deck = get_random_card(deck)
                        player.add_card(random_card)
                for player in players:
                    player.show_cards(screen)
                    player.display_score_bj(screen)
                    pygame.display.update()
                    sleep(1)

                if player0.cards is None:
                    player0.cards = []
                while len(player0.cards) < 2:
                    random_card, deck = get_random_card(deck)
                    player0.add_card(random_card)
                    player0.show_cards(screen)
                    player0.display_score_bj(screen)
                    pygame.display.update()
                    sleep(1)

                if not player0.value_count_bj() == 21:
                    for player in players:
                        player.wants_card = True
                    deal_2_cards = False
                    deal_cards = True
                else:
                    change_bal = True
                    check_results = True
                    deal_2_cards = False

            if deal_cards:
                if i < len(players):
                    if players[i].wants_card:
                        if players[i].value_count_bj() == 'bust':
                            players[i].wants_card = False
                        if players[i].value_count_bj() == 21:
                            playsound("Sounds/Applause.wav")
                            i += 1
                        else:
                            another_card_surf = test_font.render(players[i].name + ', do you want another card?',
                                                                 False, (0, 0, 0))
                            screen.blit(another_card_surf, another_card_surf.get_rect(midbottom=(600, 200)))
                            yes_button.draw(screen)
                            no_button.draw(screen)
                            if len(players[i].cards) == 2:
                                double_button.draw(screen)
                                for event in pygame.event.get():
                                    if button_pressed(yes_button, event):
                                        random_card, deck = get_random_card(deck)
                                        players[i].add_card(random_card)
                                        players[i].show_cards(screen)
                                        players[i].display_score_bj(screen)
                                    elif button_pressed(no_button, event):
                                        players[i].wants_card = False
                                    elif button_pressed(double_button, event):
                                        players[i].bet = players[i].bet*2
                                        random_card, deck = get_random_card(deck)
                                        players[i].add_card(random_card)
                                        players[i].show_cards(screen)
                                        players[i].display_score_bj(screen)
                                        players[i].wants_card = False
                                    elif button_pressed(exit_button, event):
                                        return 'Done'
                            else:
                                for event in pygame.event.get():
                                    if button_pressed(yes_button, event):
                                        random_card, deck = get_random_card(deck)
                                        players[i].add_card(random_card)
                                        players[i].show_cards(screen)
                                        players[i].display_score_bj(screen)
                                    elif button_pressed(no_button, event):
                                        players[i].wants_card = False
                                    elif button_pressed(exit_button, event):
                                        return 'Done'
                        if i >= len(players):
                            pass
                        else:
                            if not players[i].wants_card:
                                i += 1
                else:
                    dealer_cards = True

            if dealer_cards:
                while 0 < player0.value_count_bj() < 17:
                    player0.show_cards(screen, True)
                    player0.display_score_bj(screen, True)
                    pygame.display.update()
                    sleep(1)
                    random_card, deck = get_random_card(deck)
                    player0.add_card(random_card)
                deal_cards = False
                dealer_cards = False
                change_bal = True
                check_results = True

            if change_bal:
                dealer_score = player0.value_count_bj()
                for player in players:
                    player.adjust_balance(dealer_score, 'bj')
                change_bal = False

            if check_results:
                dealer_score = player0.value_count_bj()
                dealer_blackjack = False
                pygame.draw.rect(screen, (31, 171, 57), (0, 360, 1200, 25), 0)
                if dealer_score == 21 and len(player0.cards) == 2:
                    dealer_blackjack = True
                for player in players:
                    player.display_results(screen, dealer_score, 'bj', dealer_blackjack)
                player0.show_cards(screen, True)
                player0.display_score_bj(screen, True)
                again_button.draw(screen)
                for event in pygame.event.get():
                    if button_pressed(again_button, event):
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
                        deck = load_random_deck()
                    elif button_pressed(exit_button, event):
                        return 'Done'

            exit_button.draw(screen)

        else:
            screen.fill((31, 171, 57))
            screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600, 150)))
            start_button.draw(screen)
            rules_button.draw(screen)
            H = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Hearts.png"), 0, 0.15)
            S = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Spades.png"), 0, 0.15)
            screen.blit(pygame.transform.rotozoom(H, 10, 1), (510, 250))
            screen.blit(pygame.transform.rotozoom(S, -10, 1), (590, 250))
            if rules:
                pygame.draw.rect(screen, (31, 171, 57), (0, 0, 1200, 600))
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1200, 600), 2, 1)
                exit_button.draw(screen)
                splittedcontent = content.splitlines()
                x = 10
                y = 10
                for i, line in enumerate(splittedcontent):
                    rules_surf = test_font_small.render(line, False, (0, 0, 0))
                    screen.blit(rules_surf, rules_surf.get_rect(topleft=(x, y)))
                    y += 12

            for event in pygame.event.get():
                exit_pygame(event)
                if button_pressed(start_button, event):
                    game_active = True
                if not rules:
                    if button_pressed(rules_button, event):
                        rules = True
                elif button_pressed(exit_button, event):
                    rules = False

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    blackjack(screen, clock)
