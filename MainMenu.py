import pygame
from Button import Button,exit_pygame
from BlackJackClass import Blackjack, home_screen, blackjack
from HigherLower import higherlower
from AudioPlay import playsound
from Player import Player, add_player, Library
from localdirectory import local_directory
from facenet_facerecognition import create_folder
from facenet_facerecognition import clear_folder_contents
from facenet_facerecognition import PlayerRegistration
from gestures_mediapipe import LandmarkGetter
import os
"""
to do:
-scherm gesture recognition weergeven
"""


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()

    font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
    font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)
    small_font = pygame.font.SysFont('comicsans', 20)
    BLACK = (0, 0, 0)

    bj_button = Button((0, 0, 0), (300, 480), (180, 65), 'Blackjack')
    hl_button = Button((0, 0, 0), (550, 480), (260, 65), 'Higher Lower')
    newpl_button = Button((0, 0, 0), (1080, 20), (100, 25), 'New Players', 'small')
    skip_button = Button((0, 0, 0), (650, 340), (70, 25), 'Skip', 'small')

    buttons = {
        "start": Button(BLACK, (550, 480), (100, 65), 'Play!'),
        "hit": Button(BLACK, (330, 250), (110, 60), 'Hit'),
        "double": Button(BLACK, (475, 250), (250, 60), 'Double Down'),
        "stand": Button(BLACK, (770, 250), (110, 60), 'Stand'),
        "again": Button(BLACK, (530, 260), (200, 65), 'Play again!'),
        "exit": Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small'),
        "rules": Button(BLACK, (1140, 560), (40, 20), 'Rules', 'small'),
        "bet": [(i * 1000, Button(BLACK, (325 + i * 75, 300), (50, 30), f'{i}k')) for i in range(1, 6)],
        "restart": Button(BLACK, (480, 260), (250, 65), 'Restart Game')
    }
    camera = False
    with_rasp = False
    with_linking = False

    players = []

    choose_game = font_big.render('Choose Game', False, (0, 0, 0))

    library = Library()

    libraryexists_surf = small_font.render('A face library already exists for this player. Do you want to replace it?', False, (0, 0, 0))
    newlibrary_surf = small_font.render('A face library doesnt yet exists for this player. Do you want to create one?', False, (0, 0, 0))
    playeralreadyregistered = None
    yes_button = Button((0, 0, 0), (460, 300), (55, 30), 'Yes', 'small')
    no_button = Button((0, 0, 0), (700, 300), (55, 30), 'No', 'small')

    addplayers = True
    bool = False
    name_text = ''
    landmarkgetter = LandmarkGetter()
    while True:
        pygame.display.update()
        screen.fill((31, 171, 57))
        if addplayers:
            if playeralreadyregistered is None:
                if len(players) > 0:
                    skip_button.draw(screen)
                bool, name_text = add_player(screen, players, skip_button, bool, name_text, library)

                # library creation
                if not bool and name_text is not None and len(name_text) > 0 and name_text in os.listdir(library.directory) and \
                        len(os.listdir(os.path.join(library.directory, name_text))) > 0:
                    playeralreadyregistered = True
                elif not bool and name_text is not None and len(name_text) > 0:
                    playeralreadyregistered = False
            else:
                if playeralreadyregistered:
                    screen.blit(libraryexists_surf, libraryexists_surf.get_rect(topleft=(290, 250)))
                    yes_button.draw(screen)
                    no_button.draw(screen)
                    for event in pygame.event.get():
                        if yes_button.button_pressed(event):
                            clear_folder_contents(os.path.join(library.directory, name_text))
                            library.registerplayer(name_text)
                            playeralreadyregistered = None
                            name_text = ''
                        if no_button.button_pressed(event):
                            playeralreadyregistered = None
                            name_text = ''
                else:
                    screen.blit(newlibrary_surf, newlibrary_surf.get_rect(topleft=(290, 250)))
                    yes_button.draw(screen)
                    no_button.draw(screen)
                    for event in pygame.event.get():
                        if yes_button.button_pressed(event):
                            library.registerplayer(name_text)
                            playeralreadyregistered = None
                            name_text = ''
                        if no_button.button_pressed(event):
                            playeralreadyregistered = None
                            name_text = ''

            if len(players) == 4 or bool == 'skip':
                addplayers = False
        else:
            screen.blit(choose_game, choose_game.get_rect(midbottom=(600, 150)))
            bj_button.draw(screen)
            hl_button.draw(screen)
            newpl_button.draw(screen)

            for event in pygame.event.get():
                exit_pygame(event)
                if bj_button.button_pressed(event):
                    playing = True
                    playsound("Sounds/DroppingChips.wav")
                    print(players, "2")
                    while playing:
                        game = Blackjack(screen, home_screen, players, buttons, Library(), camera, with_rasp, with_linking)
                        remaining_players = blackjack(game, screen, buttons)
                        if remaining_players is not None:
                            playing = False
                elif hl_button.button_pressed(event):
                    playsound("Sounds/DroppingChips.wav")
                    players = higherlower(screen, clock, players, library, landmarkgetter)
                elif newpl_button.button_pressed(event):
                    addplayers = True
                    bool = False
                    name_text = ''
                    players = []

        clock.tick(60)


if __name__ == '__main__':
    main_menu()
