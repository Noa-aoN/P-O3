import pygame
from time import perf_counter, sleep
from Button import Button, exit_pygame
from Game import Higherlower, home_screen_hl, restart_game_screen
from Player import Player
from Style import font_big, font, font_small, WHITE, BLACK, GREEN
from Camera import init_camera, opencv_to_pygame
from gestures_mediapipe import check_index, check_all_fingers, hand_position
from mediapipe_pose import linkfacewithhand
from BlackJackClass import face_gest_crop, get_landmark_list

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


def bets_screen(game, screen, buttons):
    game.show_each_player()
    buttons["exit"].draw(screen)
    current_player = game.get_current_player()

    if not game.cap_gest:
        game.cap_gest = init_camera(0)

    if perf_counter() - game.gest_time >= 2:
        game.cameracooldown = True

    ret, img = game.cap_gest.read()

    if current_player.wants_bet:
        current_player.draw_bet_buttons(screen, buttons["bet"])

        landmarklist = game.landmarkgetter(img)
        if current_player.name in game.library.libraryembeddings:
            landmarklist, img = get_landmark_list(img, game, screen, landmarklist)

        if game.cameracooldown:
            if landmarklist:
                amt_fingers, ges_name = check_all_fingers(landmarklist[0])
                if amt_fingers:
                    bal = current_player.balance
                    if bal >= amt_fingers * 1000 and game.last_fingers == amt_fingers:
                        print("Confirmed")
                        current_button = buttons["bet"][amt_fingers - 1][1]
                        current_button.set_color((255, 0, 0))
                        current_button.draw(screen)
                        pygame.display.update()
                        sleep(0.2)
                        current_player.bet = amt_fingers * 1000
                        current_player.wants_bet = False

                    elif game.last_fingers != amt_fingers:
                        print(f"{ges_name}", end="->")
                        if game.last_fingers:
                            last_button = buttons["bet"][game.last_fingers - 1][1]
                            last_button.set_color(BLACK)
                            last_button.draw(screen)

                    current_button = buttons["bet"][amt_fingers - 1][1]
                    current_button.set_color(WHITE)
                    current_button.draw(screen)

                game.last_fingers = amt_fingers

            game.cameracooldown = False
            game.gest_time = perf_counter()

    else:
        if not current_player.wants_restart:
            game.next_player()
        game.last_fingers = None
        for _, button in buttons["bet"]:
            button.set_color(BLACK)

    img = opencv_to_pygame(img)
    surface = pygame.surfarray.make_surface(img)
    scale = pygame.transform.rotozoom(surface, -90, 1 / 8)
    screen.blit(scale, scale.get_rect(topleft=(45 + 290 * current_player.number, 415)))

    if all([not player.wants_bet for player in game.players]):
        current_player.wants_restart = False
        print("Loading Screen")
        game.draw_screen = playing_screen


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
        active_button.set_color((255, 0, 0))
        active_button.draw(screen)
        pygame.display.update()
        sleep(0.2)
        active_button.set_color(BLACK)
        active_button.draw(screen)
        pygame.display.update()
        if not wrong:
            player.prev_prize = player.prize_money
            player.calculate_prize_money()

    # This shows what button this gesture WOULD press
    elif selected_button:
        selected_button.set_color(WHITE)
        selected_button.draw(screen)

    img = opencv_to_pygame(img)
    surface = pygame.surfarray.make_surface(img)
    scale = pygame.transform.rotozoom(surface, -90, 0.25)
    screen.blit(scale, scale.get_rect(midbottom=(180, 200)))
    player.show_name(screen)
    player.show_cards(screen)
    player.display_score_hl(screen)
    player.show_prize_money(screen)
    buttons["exit"].draw(screen)
    buttons["higher"].draw(screen)
    buttons["lower"].draw(screen)

    if wrong:
        player.balance += player.prize_money - player.bet
        player.reset_money()
        game.draw_screen = wrong_screen


def wrong_screen(game, screen, buttons):
    player = game.get_current_player()
    player.show_name(screen)
    player.show_cards(screen)
    player.show_prize_money(screen)
    player.display_score_hl(screen)

    current_card = player.cards[-1]
    screen.blit(pygame.transform.rotozoom(current_card.load_image(), 0, 2), (520, 200))

    wrong_surf = font_big.render('Wrong!', False, BLACK)
    screen.blit(wrong_surf, wrong_surf.get_rect(midbottom=(600, 150)))

    if player.balance >= 1000:
        buttons["try"].draw(screen)
    buttons["next"].draw(screen)
    buttons["exit"].draw(screen)


def higherlower(game, screen, buttons):
    while True:
        game()
        templist = list(filter(lambda player: player.balance >= 1000, game.players))
        for event in pygame.event.get():
            exit_pygame(event)
            current_screen = game.draw_screen
            if not templist:
                game.draw_screen = restart_game_screen
            else:
                current_player = game.get_current_player()

            # Home Screen
            if current_screen == home_screen_hl:
                if buttons["start"].button_pressed(event):
                    game.draw_screen = bets_screen
                elif buttons["rules"].button_pressed(event):
                    game.draw_screen = rules_screen
                elif buttons["exit"].button_pressed(event):
                    return game.players

            # Rules Screen
            elif current_screen == rules_screen:
                if buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_hl

            # Betting Screen
            elif current_screen == bets_screen:
                bal = current_player.balance
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_hl

                for bet_amount, button in game.buttons["bet"]:
                    if button.button_pressed(event) and bal >= bet_amount:
                        current_player.bet = bet_amount
                        current_player.wants_bet = False

            # Playing Screen
            elif current_screen == playing_screen:
                if current_player.balance < 1000:
                    game.play_again(current_player)
                    game.next_player()
                if buttons["exit"].button_pressed(event):
                    current_player.wants_restart = True
                    game.draw_screen = home_screen_hl
                elif buttons["higher"].button_pressed(event) or buttons["lower"].button_pressed(event):
                    game.give_card()
                    game.deck = game.get_card_func(game, current_player)
                    current_player.show_cards(screen)
                    last_val, current_val = last_two_vals(current_player)

                    high = buttons["higher"].button_pressed(event) and last_val > current_val
                    low = buttons["lower"].button_pressed(event) and last_val < current_val

                    if high or low:
                        current_player.balance += current_player.prize_money - current_player.bet
                        current_player.reset_money()
                        game.draw_screen = wrong_screen
                    else:
                        current_player.prev_prize = current_player.prize_money
                        current_player.calculate_prize_money()

            # Wrong Screen
            elif current_screen == wrong_screen:
                if buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_hl
                elif buttons["next"].button_pressed(event):
                    prev_idx = game.player_index
                    game.play_again(current_player)
                    game.next_player()
                    if prev_idx == len(game.players)-1:
                        game.draw_screen = bets_screen
                    else:
                        game.draw_screen = playing_screen
                elif current_player.balance >= 1000:
                    if buttons["try"].button_pressed(event) and current_player.balance >= 1000:
                        current_player.wants_restart = True
                        game.play_again(current_player)
                        game.draw_screen = bets_screen

            # Restart Game Screen
            elif current_screen == restart_game_screen:
                game.play_again()
                if buttons["restart"].button_pressed(event):
                    for i in game.players:
                        i.balance = 10000
                    game.draw_screen = bets_screen
                    return None
                elif buttons["exit"].button_pressed(event):
                    return game.players


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))

    names = ['Nowa', 'Karel', 'Yannic', 'Jasper']
    players = [Player(name, 10000, i) for i, name in enumerate(names)]

    buttons = {
        "start": Button(BLACK, (550, 480), (100, 65), 'Play!'),
        "bet": [(i * 1000, Button(BLACK, (325 + i * 75, 300), (50, 30), f'{i}k')) for i in range(1, 6)],
        "higher": Button(BLACK, (380, 250), (150, 60), 'Higher'),
        "lower": Button(BLACK, (680, 250), (150, 60), 'Lower'),
        "try": Button(BLACK, (480, 480), (240, 65), 'Try again'),
        "exit": Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small'),
        "rules": Button(BLACK, (1140, 560), (40, 20), 'Rules', 'small'),
        "restart": Button(BLACK, (530, 260), (200, 65), 'Restart Game'),
        "next": Button(BLACK, (800, 480), (240, 65), 'Next player')
    }
    camera = False
    with_rasp = False
    with_linking = False
    playing = True
    while playing:
        game = Higherlower(screen, players, buttons, camera, with_rasp, with_linking)
        remaining_players = higherlower(game, screen, buttons)
        if remaining_players is None:
            print("restarting game")
        else:
            playing = False
            print("Game Ended", remaining_players)