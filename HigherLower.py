from sys import exit
from random import choice
from Button import Button, button_pressed, exit_pygame
from Deck import *
from Player import Player
import time

test_font_big = pygame.font.SysFont('comicsans', 80)
test_font = pygame.font.SysFont('comicsans', 25)

Higherlower_surf = test_font_big.render('Higher Lower', False, (0, 0, 0))
False_surf = test_font_big.render('Wrong!', False, (0, 0, 0))


def add_new_card(deck, player):
    random_card = choice(deck)
    deck.remove(random_card)
    player.add_card(random_card)


def last_two_cards(player):
    aantal_kaarten = len(player.cards)-1

    vorige_kaart = player.cards[aantal_kaarten-1]
    huidige_kaart = player.cards[aantal_kaarten]

    return vorige_kaart, huidige_kaart


def wrong_guess(player, huidige_kaart, window):
    window.fill((31, 171, 57))
    window.blit(False_surf, False_surf.get_rect(midbottom=(600, 150)))
    player.show_cards(window)
    window.blit(pygame.transform.rotozoom(huidige_kaart.load_image(), 0, 2), (520, 200))
    pygame.display.update()
    time.sleep(3)


def higherlower(screen, clock):
    screen.fill((31, 171, 57))
    player_deck = load_deck()
    player1 = Player('Matthias', 10000, 1)
    game_active = False

    start_button = Button((0, 0, 0), (550, 480), (100, 65), 'Play!')
    again_button = Button((0, 0, 0), (480, 480), (240, 65), 'Play again?')
    high_button = Button((0, 0, 0), (380, 250), (150, 60), 'Higher')
    low_button = Button((0, 0, 0), (680, 250), (150, 60), 'Lower')
    exit_button = Button((0, 0, 0), (1140, 20), (40, 20), 'Exit', 'small')
    lost = False

    while True:
        pygame.display.update()
        if game_active:
            if not lost:
                screen.fill((31, 171, 57))
                player1.show_name(screen)
                player1.display_score_hl(screen)

                if len(player1.cards) < 1:
                    add_new_card(player_deck, player1)

                player1.show_cards(screen)
                pick_higher_lower_surf = test_font.render(
                    f'{player1.name}, is the next card going to be higher or lower?', False, (0, 0, 0))
                screen.blit(pick_higher_lower_surf, pick_higher_lower_surf.get_rect(midbottom=(600, 200)))
                high_button.draw(screen)
                low_button.draw(screen)

                for event in pygame.event.get():
                    if button_pressed(high_button, event) or button_pressed(low_button, event):
                        add_new_card(player_deck, player1)
                        player1.show_cards(screen)
                        vorige, huidige = last_two_cards(player1)

                        high = button_pressed(high_button, event) and vorige.hl_value > huidige.hl_value
                        low = button_pressed(low_button, event) and vorige.hl_value < huidige.hl_value
                        if high or low:
                            lost = True
                            wrong_guess(player1, huidige, screen)

                    elif button_pressed(exit_button, event):
                        return 'Done'
            else:
                screen.fill((31, 171, 57))
                again_button.draw(screen)

                for event in pygame.event.get():
                    if button_pressed(again_button, event):
                        player1.cards = []
                        player_deck = load_deck()
                        lost = False

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
