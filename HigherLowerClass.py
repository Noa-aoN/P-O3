import pygame
from time import perf_counter
from Button import exit_pygame
from Game import Higherlower, home_screen_hl
from Player import Player
from Style import font_huge, font, WHITE, BLACK, GREEN
from Camera import init_camera, opencv_to_pygame
from BlackJackClass import get_landmark_list
from gestures_mediapipe import check_index

'''
Bugs: 
- waarschijnlijk wel

To DO:
- een oplossing verzinnen voor meerdere spelers te displayen
- zie BlackJackClass
'''


def last_two_vals(player):
    assert len(player.cards) >= 2
    last_card = player.cards[-2]
    current_card = player.cards[-1]
    return last_card.hl_value, current_card.hl_value


def rules_screen(game, screen, buttons):
    f = open('RulesHigherLower', 'r')
    content = f.read()
    split_content = content.splitlines()
    pygame.draw.rect(screen, GREEN, (0, 0, 1200, 600))
    for i, line in enumerate(split_content):
        rules_surf = font.render(line, False, BLACK)
        screen.blit(rules_surf, rules_surf.get_rect(topleft=(10, 10 + i * 30)))
    f.close()
    buttons["exit"].draw(screen)


def playing_screen(game, screen, buttons):
    player = game.get_current_player()

    # Give the current player a card if they have none
    if not player.cards:
        game.give_card()
        game.deck = game.get_card_func(game, player)

    question_surf = font.render(f'{player.name}, is the next card going to be higher or lower?', False, BLACK)
    screen.blit(question_surf, question_surf.get_rect(midbottom=(600, 200)))

    if not game.cap_gest:
        game.cap_gest = init_camera(0)

    if perf_counter() - game.gest_time >= 2:
        game.cameracooldown = True

    ret, img = game.cap_gest.read()
    landmarklist = game.landmarkgetter(img)
    active_button = None
    selected_button = None
    wrong = False

    if player.name in game.library.libraryembeddings:
        landmarklist, img = get_landmark_list(img, game, screen, landmarklist)

    if game.cameracooldown:
        if landmarklist:
            index = check_index(landmarklist[0])
            if index == "index up":
                if game.last_index == index:
                    game.deck = game.get_card_func(game, player)
                    last_val, current_val = last_two_vals(player)
                    wrong = last_val > current_val
                    active_button = buttons["higher"]
                else:
                    selected_button = buttons["higher"]

            elif index == "index down":
                if game.last_index == index:
                    game.deck = game.get_card_func(game, player)
                    last_val, current_val = last_two_vals(player)
                    wrong = last_val < current_val
                    active_button = buttons["lower"]
                else:
                    selected_button = buttons["lower"]

            game.last_index = index
            game.cameracooldown = False
            game.gest_time = perf_counter()

    # If a button is "pressed"
    if active_button:
        active_button.set_color(BLACK)
        active_button.draw(screen)

    # This shows what button this gesture WOULD press
    elif selected_button:
        selected_button.set_color(WHITE)
        selected_button.draw(screen)

    if wrong:
        game.draw_screen = wrong_screen

    img = opencv_to_pygame(img)
    surface = pygame.surfarray.make_surface(img)
    scale = pygame.transform.rotozoom(surface, -90, 0.25)
    screen.blit(scale, scale.get_rect(midbottom=(180, 200)))
    player.show_name(screen)
    player.show_cards(screen)
    player.display_score_hl(screen)
    buttons["exit"].draw(screen)
    buttons["higher"].draw(screen)
    buttons["lower"].draw(screen)


def wrong_screen(game, screen, buttons):
    player = game.get_current_player()
    player.show_name(screen)
    player.show_cards(screen)
    player.display_score_hl(screen)

    current_card = player.cards[-1]
    screen.blit(pygame.transform.rotozoom(current_card.load_image(), 0, 2), (520, 200))

    wrong_surf = font_huge.render('Wrong!', False, BLACK)
    screen.blit(wrong_surf, wrong_surf.get_rect(midbottom=(600, 150)))

    buttons["try"].draw(screen)
    buttons["next"].draw(screen)


def higherlower(game):
    while True:
        game()
        screen = game.screen
        for event in pygame.event.get():
            exit_pygame(event)
            current_screen = game.draw_screen
            current_player = game.get_current_player()

            # Home Screen
            if current_screen == home_screen_hl:
                if game.buttons["start"].button_pressed(event):
                    game.draw_screen = playing_screen
                elif game.buttons["rules"].button_pressed(event):
                    game.draw_screen = rules_screen
                elif game.buttons["cam"].button_pressed(event):
                    game.cam = not game.cam
                    print("camera", game.cam)
                    if game.cam:
                        game.buttons["cam"].set_color(WHITE)
                    else:
                        game.buttons["cam"].set_color(BLACK)
                    #game.buttons["cam"].draw(screen)
                    #pygame.display.update()
                elif game.buttons["rasp"].button_pressed(event):
                    game.rasp = not game.rasp
                    print("raspberry pi", game.rasp)
                    if game.rasp:
                        game.buttons["rasp"].set_color(WHITE)
                    else:
                        game.buttons["rasp"].set_color(BLACK)
                    #game.buttons["rasp"].draw(screen)
                    #pygame.display.update()
                elif game.buttons["link"].button_pressed(event):
                    game.with_linking = not game.with_linking
                    print("face linking", game.with_linking)
                    if game.with_linking:
                        game.buttons["link"].set_color(WHITE)
                    else:
                        game.buttons["link"].set_color(BLACK)
                    #game.buttons["link"].draw(screen)
                    #pygame.display.update()
                elif game.buttons["exit"].button_pressed(event):
                    return game.players

            # Rules Screen
            elif current_screen == rules_screen:
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_hl

            # Playing Screen
            elif current_screen == playing_screen:
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_hl
                elif game.buttons["higher"].button_pressed(event) or game.buttons["lower"].button_pressed(event):
                    game.give_card()
                    game.deck = game.get_card_func(game, current_player)
                    current_player.show_cards(screen)
                    last_val, current_val = last_two_vals(current_player)

                    high = game.buttons["higher"].button_pressed(event) and last_val > current_val
                    low = game.buttons["lower"].button_pressed(event) and last_val < current_val

                    if high or low:
                        game.draw_screen = wrong_screen

            # Wrong Screen
            elif current_screen == wrong_screen:
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_hl
                elif game.buttons["try"].button_pressed(event):
                    game.play_again()
                    game.draw_screen = playing_screen
                elif game.buttons["next"].button_pressed(event):
                    game.next_player()
                    game.play_again()
                    game.draw_screen = playing_screen


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))

    names = ['Nowa', 'Karel', 'Yannic', 'Jasper']
    players = [Player(name, 10000, i) for i, name in enumerate(names)]

    playing = True
    while playing:
        game = Higherlower(screen, players)
        remaining_players = higherlower(game)
        if remaining_players is None:
            print("restarting game")
        else:
            playing = False
            print("Game Ended", remaining_players)
