from sys import exit
import random
from Button import Button, button_pressed, exit_pygame
from Deck import *
from Player import Player
import time


def higherlower(screen, clock):
    test_font_big = pygame.font.SysFont('comicsans', 80)
    test_font = pygame.font.SysFont('comicsans', 25)

    Higherlower_surf = test_font_big.render('Higher Lower', False, (0, 0, 0))
    False_surf = test_font_big.render('False!', False, (0, 0, 0))

    screen.fill((31, 171, 57))
    player_deck = deck
    players = []
    player1 = Player('Matthias', 10000, 1)
    players.append(player1)
    game_active = False

    start_button = Button((0, 0, 0), (550, 480), (100, 65), 'Play!')
    again_button = Button((0, 0, 0), (480, 480), (240, 65), 'Play again?')
    high_button = Button((0, 0, 0), (380, 250), (150, 60), 'Higher')
    low_button = Button((0, 0, 0), (680, 250), (150, 60), 'Lower')
    exit_button = Button((0, 0, 0), (1140, 20), (40, 20), 'Exit', 'small')
    deal_card = True
    verloren = False
    while True:
        pygame.display.update()

        if game_active:
            if not verloren:
                screen.fill((31, 171, 57))
                player1.show_name(screen)
                player1.display_score_hl(screen)
                if deal_card:
                    while len(player1.cards) < 1:
                        random_card = random.choice(player_deck)
                        player_deck.remove(random_card)
                        player1.add_card(random_card)
                        aantal_kaarten = 1
                player1.show_cards(screen)
                pick_higher_lower_surf = test_font.render(
                    players[0].name + ', is the next card going to be higher or lower?',
                    False, (0, 0, 0))
                screen.blit(pick_higher_lower_surf, pick_higher_lower_surf.get_rect(midbottom=(600, 200)))
                high_button.draw(screen)
                low_button.draw(screen)
                for event in pygame.event.get():
                    if button_pressed(high_button, event):
                        random_card = random.choice(player_deck)
                        player_deck.remove(random_card)
                        players[0].add_card(random_card)
                        players[0].show_cards(screen)
                        vorige_kaart = player1.cards[aantal_kaarten - 1]
                        huidige_kaart = player1.cards[aantal_kaarten]
                        if vorige_kaart.value <= huidige_kaart.value:
                            aantal_kaarten += 1
                        else:
                            al_stil = False
                            screen.fill((31, 171, 57))
                            screen.blit(False_surf, False_surf.get_rect(midbottom=(600, 150)))
                            verloren = True
                            player1.show_cards(screen)
                            screen.blit(pygame.transform.rotozoom(player1.cards[aantal_kaarten].load_image(), 0, 2),
                                        (520, 200))

                    elif button_pressed(low_button, event):
                        random_card = random.choice(player_deck)
                        player_deck.remove(random_card)
                        players[0].add_card(random_card)
                        players[0].show_cards(screen)
                        vorige_kaart = player1.cards[aantal_kaarten - 1]
                        huidige_kaart = player1.cards[aantal_kaarten]
                        if vorige_kaart.value >= huidige_kaart.value:
                            aantal_kaarten += 1
                        else:
                            al_stil = False
                            screen.fill((31, 171, 57))
                            screen.blit(False_surf, False_surf.get_rect(midbottom=(600, 150)))
                            verloren = True
                            player1.show_cards(screen)
                            screen.blit(pygame.transform.rotozoom(player1.cards[aantal_kaarten].load_image(), 0, 2),
                                        (520, 200))
                    elif button_pressed(exit_button, event):
                        return 'Done'
            else:
                if not al_stil:
                    time.sleep(3)
                    al_stil = True
                screen.fill((31, 171, 57))
                again_button.draw(screen)

                for event in pygame.event.get():
                    if button_pressed(again_button, event):
                        player1.cards = []
                        player_deck = deck
                        verloren = False
                    if button_pressed(exit_button, event):
                        return 'Done'

            exit_button.draw(screen)

        else:
            screen.blit(Higherlower_surf, Higherlower_surf.get_rect(midbottom=(600, 150)))
            start_button.draw(screen)

            for event in pygame.event.get():
                exit_pygame(event)
                if button_pressed(start_button, event):
                    game_active = True

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    higherlower(screen, clock)
