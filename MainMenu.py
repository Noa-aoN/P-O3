import pygame
import os
from Button import Button, exit_pygame
from Game import Blackjack, Higherlower
from BlackJackClass import blackjack
from HigherLowerClass import higherlower
from AudioPlay import playsound
from Player import add_player, Library
from facenet_facerecognition import clear_folder_contents
from Style import BLACK, GREEN, font_huge, font
"""
to do:
-scherm gesture recognition weergeven

bugs: 
als ge teveel kaarten hebt bij higher lower gaat het uit uw vakje 

als ge van hoger lager naar blackjack gaat dan hebt ge nog steeds uw deck wat ge bij hoger lager geïndigd zijt.
"""


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()

    bj_button = Button(BLACK, (350, 320), (180, 65), 'Blackjack')
    hl_button = Button(BLACK, (600, 320), (260, 65), 'Higher Lower')
    newpl_button = Button(BLACK, (1080, 20), (100, 25), 'New Players', 'small')
    skip_button = Button(BLACK, (650, 340), (70, 25), 'Skip', 'small')
    yes_button = Button(BLACK, (460, 300), (55, 30), 'Yes', 'small')
    no_button = Button(BLACK, (700, 300), (55, 30), 'No', 'small')

    players = []
    library = Library()
    playeralreadyregistered = None
    addplayers = True
    bool = False
    name_text = ''

    while True:
        pygame.display.update()
        screen.fill(GREEN)
        if addplayers:
            if playeralreadyregistered is None:
                if players:
                    skip_button.draw(screen)
                bool, name_text = add_player(screen, players, skip_button, bool, name_text)

                # library creation
                if not bool and name_text is not None and len(name_text) > 0 and name_text in os.listdir(library.directory) and \
                        len(os.listdir(os.path.join(library.directory, name_text))) > 0:
                    playeralreadyregistered = True
                elif not bool and name_text is not None and len(name_text) > 0:
                    playeralreadyregistered = False
            else:
                yes_button.draw(screen)
                no_button.draw(screen)
                if playeralreadyregistered:
                    library_text = 'A face library already exists for this player. Do you want to replace it?'
                    for event in pygame.event.get():
                        if yes_button.button_pressed(event):
                            clear_folder_contents(os.path.join(library.directory, name_text))
                            library.registerplayer(name_text)
                            playeralreadyregistered = None
                            name_text = ''
                        elif no_button.button_pressed(event):
                            playeralreadyregistered = None
                            name_text = ''
                else:
                    library_text = 'A face library doesnt yet exists for this player. Do you want to create one?'
                    for event in pygame.event.get():
                        if yes_button.button_pressed(event):
                            library.registerplayer(name_text)
                            playeralreadyregistered = None
                            name_text = ''
                        elif no_button.button_pressed(event):
                            playeralreadyregistered = None
                            name_text = ''
                library_surf = font.render(library_text, False, BLACK)
                screen.blit(library_surf, library_surf.get_rect(topleft=(290, 250)))
            if (len(players) == 4 and playeralreadyregistered is None) or bool == 'skip':
                addplayers = False
        else:
            choose_game = font_huge.render('Choose Game', False, BLACK)
            screen.blit(choose_game, choose_game.get_rect(midbottom=(600, 150)))
            bj_button.draw(screen)
            hl_button.draw(screen)
            newpl_button.draw(screen)

            for event in pygame.event.get():
                exit_pygame(event)
                if bj_button.button_pressed(event):
                    playing = True
                    playsound("Sounds/DroppingChips.wav")
                    while playing:
                        game = Blackjack(screen, players)
                        remaining_players = blackjack(game)
                        if remaining_players is not None:
                            playing = False

                elif hl_button.button_pressed(event):
                    playing = True
                    playsound("Sounds/DroppingChips.wav")
                    while playing:
                        game = Higherlower(screen, players)
                        remaining_players = higherlower(game)
                        if remaining_players is not None:
                            playing = False
                elif newpl_button.button_pressed(event):
                    addplayers = True
                    bool = False
                    name_text = ''
                    players = []

        clock.tick(20)


if __name__ == '__main__':
    main_menu()
