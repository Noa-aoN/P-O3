import pygame
from Button import Button, turn_white, button_pressed, exit_pygame
from BlackJack import blackjack
from HigherLower import higherlower
from AudioPlay import playsound
from Player import Player, add_player


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()

    font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
    font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)

    bj_button = Button((0, 0, 0), (300, 480), (180, 65), 'Blackjack')
    hl_button = Button((0, 0, 0), (550, 480), (260, 65), 'Higher Lower')
    skip_button = Button((0, 0, 0), (650, 340), (70, 25), 'Skip', 'small')

    player0 = Player('Dealer', 0, 0)
    players = [player0]

    choose_game = font_big.render('Choose Game', False, (0, 0, 0))

    add_players = True
    bool = False
    name_text = ''
    while True:
        pygame.display.update()
        screen.fill((31, 171, 57))
        if add_players:
            if len(players) > 1:
                skip_button.draw(screen)
            bool, name_text = add_player(screen, players, skip_button, bool, name_text)
            if len(players) == 5 or bool == 'skip':
                add_players = False
        else:
            screen.blit(choose_game, choose_game.get_rect(midbottom=(600, 150)))
            bj_button.draw(screen)
            hl_button.draw(screen)

            for event in pygame.event.get():
                exit_pygame(event)
                if button_pressed(bj_button, event):
                    playsound("Sounds/DroppingChips.wav")
                    status_bj = blackjack(screen, clock, players)
                elif button_pressed(hl_button, event):
                    playsound("Sounds/DroppingChips.wav")
                    status_bj = higherlower(screen, clock, players)


        clock.tick(60)


if __name__ == '__main__':
    main_menu()
