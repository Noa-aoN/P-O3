import pygame
import os
from Button import Button, exit_pygame
from Game import Blackjack, Higherlower
from BlackJackClass import blackjack
from HigherLowerClass import higherlower
from AudioPlay import playsound
from Player import add_player, Library
from Detection.facenet_facerecognition import clear_folder_contents
from Style import BLACK, GREEN, font_huge, font
"""
to do:
-scherm gesture recognition weergeven

bugs: 
als ge van hoger lager naar blackjack gaat dan hebt ge nog steeds uw deck wat ge bij hoger lager geïndigd zijt.
- some buttons appear white when drawn.
"""


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
    pygame.display.set_caption('Virtual Card Game Robot')
    vtk_icon = pygame.image.load('Images/VTK_icon.png')
    pygame.display.set_icon(vtk_icon)
    clock = pygame.time.Clock()

    players = []
    library = Library()
    playeralreadyregistered = None
    addplayers = True
    bool = False
    name_text = ''

    fullscreen = True

    while True:
        w, h = pygame.display.get_surface().get_size()
        x_scale, y_scale = w / 1200, h / 600
        if ((x_scale, y_scale) != (1, 1) and not fullscreen) or ((x_scale, y_scale) == (1, 1) and fullscreen):
            bj_button = Button(BLACK, (350 * x_scale, 320 * y_scale), (180 * x_scale, 65 * y_scale), 'Blackjack')
            hl_button = Button(BLACK, (600 * x_scale, 320 * y_scale), (260 * x_scale, 65 * y_scale), 'Higher Lower')
            newpl_button = Button(BLACK, (1080 * x_scale, 20 * y_scale), (100 * x_scale, 25 * y_scale), 'New Players',
                                  'small')
            skip_button = Button(BLACK, (650 * x_scale, 340 * y_scale), (70 * x_scale, 25 * y_scale), 'Skip', 'small')
            yes_button = Button(BLACK, (460 * x_scale, 300 * y_scale), (55 * x_scale, 30 * y_scale), 'Yes', 'small')
            no_button = Button(BLACK, (700 * x_scale, 300 * y_scale), (55 * x_scale, 30 * y_scale), 'No', 'small')

            common_buttons = {
                "start": Button(BLACK, (540 * x_scale, 420 * y_scale), (150 * x_scale, 60 * y_scale), 'Play!'),
                "cam": Button(BLACK, (540 * x_scale, 490 * y_scale), (150 * x_scale, 20 * y_scale), 'Card Detection', 'small'),
                "rasp": Button(BLACK, (540 * x_scale, 520 * y_scale), (150 * x_scale, 20 * y_scale), 'Raspberry Pi', 'small'),
                "link": Button(BLACK, (540 * x_scale, 550 * y_scale), (150 * x_scale, 20 * y_scale), 'Face Authentication', 'small'),
                "restart": Button(BLACK, (470 * x_scale, 260 * y_scale), (280 * x_scale, 65 * y_scale), 'Restart Game'),
                "exit": Button(BLACK, (1140 * x_scale, 20 * y_scale), (40 * x_scale, 20 * y_scale), 'Exit', 'small'),
                "rules": Button(BLACK, (1140 * x_scale, 560 * y_scale), (40 * x_scale, 20 * y_scale), 'Rules', 'small'),
                "again": Button(BLACK, (500 * x_scale, 260 * y_scale), (200 * x_scale, 65 * y_scale), 'Play Again!'),
                "bet": [(i * 1000, Button(BLACK, (325 * x_scale + i * 75 * x_scale, 300 * y_scale), (50 * x_scale, 30 * y_scale), f'{i}k')) for i in range(1, 6)]
            }

            hl_buttons = {
                "higher": Button(BLACK, (380 * x_scale, 250 * y_scale), (150 * x_scale, 60 * y_scale), 'Higher'),
                "lower": Button(BLACK, (680 * x_scale, 250 * y_scale), (150 * x_scale, 60 * y_scale), 'Lower'),
                "try": Button(BLACK, (480 * x_scale, 480 * y_scale), (240 * x_scale, 65 * y_scale), 'Try Again', None, GREEN),
                "next": Button(BLACK, (480 * x_scale, 480 * y_scale), (240 * x_scale, 65 * y_scale), 'Next Player', None, GREEN)
            }

            bj_buttons = {
                "hit": Button(BLACK, (330 * x_scale, 250 * y_scale), (110 * x_scale, 60 * y_scale), 'Hit'),
                "double": Button(BLACK, (475 * x_scale, 250 * y_scale), (250 * x_scale, 60 * y_scale), 'Double Down'),
                "stand": Button(BLACK, (770 * x_scale, 250 * y_scale), (110 * x_scale, 60 * y_scale), 'Stand')
            }

            fullscreen = not fullscreen

        pygame.display.update()
        screen.fill(GREEN)
        if addplayers:
            if playeralreadyregistered is None:
                if players:
                    skip_button.draw(screen)
                bool, name_text = add_player(screen, players, skip_button, bool, name_text, x_scale, y_scale)

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
                screen.blit(library_surf, library_surf.get_rect(topleft=(290*x_scale, 250 * y_scale)))
            if (len(players) == 4 and playeralreadyregistered is None) or bool == 'skip':
                addplayers = False

        else:
            choose_game = font_huge.render('Choose Game', False, BLACK)
            screen.blit(choose_game, choose_game.get_rect(midbottom=(600*x_scale, 150 * y_scale)))
            bj_button.draw(screen)
            hl_button.draw(screen)
            newpl_button.draw(screen)

            for event in pygame.event.get():
                exit_pygame(event)
                if bj_button.button_pressed(event):
                    playing = True
                    playsound("Sounds/DroppingChips.wav")
                    while playing:
                        game = Blackjack(screen, players, dict(common_buttons, **bj_buttons), x_scale, y_scale)
                        players = blackjack(game)
                        if players is not None:
                            playing = False

                elif hl_button.button_pressed(event):
                    playing = True
                    playsound("Sounds/DroppingChips.wav")
                    while playing:
                        game = Higherlower(screen, players, dict(common_buttons, **hl_buttons), x_scale, y_scale)
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
