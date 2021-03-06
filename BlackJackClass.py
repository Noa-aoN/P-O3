import pygame
from time import sleep, perf_counter
from Button import exit_pygame
from Player import Player
from Game import Blackjack, home_screen_bj, restart_game_screen
from AudioPlay import playsound
from Detection.face_with_hand_linking import get_landmark_list
from Detection.gestures_mediapipe import check_all_fingers, check_option
from Camera import init_camera, opencv_to_pygame
from Style import font, font2_small, WHITE, BLACK, GREEN


def rules_screen(game, screen, buttons, x_scale, y_scale):
    buttons["exit"].draw(screen)
    f = open('Rules/RulesBlackjack.txt', 'r')
    content = f.read()
    split_content = content.splitlines()
    for i, line in enumerate(split_content):
        rules_surf = font2_small.render(line, False, BLACK)
        screen.blit(rules_surf, rules_surf.get_rect(topleft=(10*x_scale, 3*y_scale + i * 20*y_scale)))
    f.close()


def bets_screen(game, screen, buttons, x_scale, y_scale):
    game.show_each_player()

    buttons["exit"].draw(screen)

    current_player = game.get_current_player()

    if int(current_player.number) != int(game.previous_player):
        game.rotate_fromto_player(game.previous_player, current_player.number)

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
        game.next_player()
        game.last_fingers = None
        for _, button in buttons["bet"]:
            button.set_color(BLACK)

    img = opencv_to_pygame(img)
    surface = pygame.surfarray.make_surface(img)
    scale = pygame.transform.rotozoom(surface, -90, 1 / 8)
    screen.blit(scale, scale.get_rect(topleft=(45*x_scale + 290*x_scale * current_player.number, 415*y_scale)))

    if all([not player.wants_bet for player in game.players]) and game.player_index == game.players[0].number:
        print("Loading Screen")
        game.draw_screen = deal_cards_screen
    if all([len(player.cards) == 2 for player in game.players]):
        game.draw_screen = playing_screen


def deal_cards_screen(game, screen, buttons, x_scale, y_scale):
    # Put the balances on the screen
    game.show_each_player()
    pygame.display.update()

    for player in game.players:
        for _ in range(2):
            if game.previous_player != player.number:
                game.rotate_fromto_player(game.previous_player, player.number)

            game.get_card_func(player)
            screen.fill(GREEN)
            game.show_each_player()
            pygame.display.update()
            sleep(0.5)

    # Give the dealer 2 cards
    # 1 face-up, 1 face-down
    if game.previous_player != 1.5:
        game.rotate_fromto_player(game.previous_player, 1.5)

    game.get_card_func(game.dealer)
    game.dealer.show_cards(screen)
    game.dealer.display_score_bj(screen)
    pygame.display.update()
    sleep(0.5)
    game.dealer.add_hidden_card()
    game.dealer.show_cards(screen)
    pygame.display.update()

    assert all([len(player.cards) == 2 for player in game.players])
    assert len(game.dealer.cards) == 2

    # Zet de servo terug naar de eerste speler
    # print("RESET SERVO")
    game.rotate_fromto_player(game.previous_player, game.get_current_player().number)

    print("Playing Screen")
    game.draw_screen = playing_screen


def playing_screen(game, screen, buttons, x_scale, y_scale):
    game.show_each_player()

    game.dealer.show_cards(screen)
    game.dealer.display_score_bj(screen)
    #buttons["exit"].draw(screen)

    current_player = game.get_current_player()
    library = game.library

    if int(current_player.number) != int(game.previous_player):
        game.rotate_fromto_player(game.previous_player, current_player.number)

    ret, img = game.cap_gest.read()

    if perf_counter() - game.gest_time >= 2:
        game.cameracooldown = True

    if current_player.wants_card:
        if current_player.value_count_bj() == 0:
            print(f"{current_player} Busted")
            playsound("Sounds/Bust.wav")
            current_player.wants_card = False

        elif current_player.value_count_bj() == 21:
            print(f"{current_player} got Blackjack")
            playsound("Sounds/Applause.wav")
            current_player.wants_card = False

        else:
            another_card_surf = font.render(f'{current_player.name}, do you want another card?', False, BLACK)
            screen.blit(another_card_surf, another_card_surf.get_rect(midbottom=(600*x_scale, 200*y_scale)))

            buttons["hit"].draw(screen)
            buttons["stand"].draw(screen)
            if double_down := len(current_player.cards) == 2 and current_player.balance >= 2 * current_player.bet:
                buttons["double"].draw(screen)

            landmarklist = game.landmarkgetter(img)
            if current_player.name in library.libraryembeddings:
                landmarklist, img = get_landmark_list(img, game, screen, landmarklist)

            if game.cameracooldown:
                if landmarklist:
                    option = check_option(landmarklist[0], double_down)
                    if option:
                        if game.last_option == option and option is not None:
                            print("Confirmed")
                            current_button = buttons[option]
                            current_button.set_color((255, 0, 0))
                            current_button.draw(screen)
                            pygame.display.update()
                            sleep(0.2)
                            if option == "hit":
                                game.get_card_func(current_player)
                                current_player.show_cards(screen)
                                current_player.display_score_bj(screen)

                            elif option == "double" and len(current_player.cards) == 2 and \
                                    current_player.balance >= 2 * current_player.bet:
                                current_player.bet = current_player.bet * 2
                                game.get_card_func(current_player)
                                current_player.show_cards(screen)
                                current_player.display_score_bj(screen)
                                current_player.wants_card = False

                            elif option == "stand":
                                current_player.wants_card = False

                        # Last two options weren't the same
                        else:
                            print(f"{option}", end="->")
                            if game.last_option:
                                last_button = buttons.get(game.last_option)
                                last_button.set_color(BLACK)
                                last_button.draw(screen)

                        current_button = buttons.get(option)
                        current_button.set_color(WHITE)
                        current_button.draw(screen)

                    game.last_option = option

                game.cameracooldown = False
                game.gest_time = perf_counter()
    else:
        game.next_player()
        for option in ("hit", "stand", "double"):
            buttons[option].set_color(BLACK)
        game.last_option = None

    img = opencv_to_pygame(img)
    surface = pygame.surfarray.make_surface(img)
    scale = pygame.transform.rotozoom(surface, -90, 1 / 8)
    screen.blit(scale, scale.get_rect(topleft=(45*x_scale + 290*x_scale * current_player.number, 415*y_scale)))

    if all([not player.wants_card for player in game.players]) and game.player_index == game.players[0].number:
        #print("Dealer Cards Screen")
        game.draw_screen = dealer_card_screen


def check_results_screen(game, screen, buttons, x_scale, y_scale):
    game.show_each_player()

    game.dealer.show_cards(screen)
    game.dealer.display_score_bj(screen)
    buttons["exit"].draw(screen)
    buttons["again"].draw(screen)

    dealer_score = game.dealer.value_count_bj()
    dealer_blackjack = dealer_score == 21 and len(game.dealer.cards) == 2

    pygame.draw.rect(screen, GREEN, (0, 340*y_scale, 1200*x_scale, 25*y_scale), 0)
    for player in game.players:
        player.display_results(screen, dealer_score, 'bj', dealer_blackjack)
        if dealer_blackjack:
            player.adjust_balance(dealer_score, 'bj', dealer_blackjack)

    game.dealer.show_cards(screen)
    game.dealer.display_score_bj(screen, dealer_blackjack)


def dealer_card_screen(game, screen, buttons, x_scale, y_scale):
    game.show_each_player()
    if game.dealer.has_dummy:
        game.dealer.cards.pop()
        game.dealer.has_dummy = False
    game.dealer.show_cards(screen)
    game.dealer.display_score_bj(screen)

    not_everyone_busts = not game.everyone_bust()
    if not_everyone_busts:
        # Rotate to dealer
        game.rotate_fromto_player(game.previous_player, 1.5)
        while 0 < game.dealer.value_count_bj() < 17:
            game.dealer.show_cards(screen)
            game.dealer.display_score_bj(screen)
            pygame.display.update()
            sleep(1)
            game.get_card_func(game.dealer)
    dealer_score = game.dealer.value_count_bj()

    for player in game.players:
        player.adjust_balance(dealer_score, 'bj')

    print("Checking Results")
    game.draw_screen = check_results_screen


def blackjack(game):
    while True:
        # Call the game class to display the current frame
        game()
        templist = list(filter(lambda player: player, game.players))
        screen = game.screen
        for event in pygame.event.get():
            exit_pygame(event)
            current_screen = game.draw_screen
            if not templist:
                current_screen = restart_game_screen
            if current_screen != restart_game_screen:
                current_player = game.get_current_player()

            # Home Screen
            if current_screen == home_screen_bj:
                if game.buttons["rules"].button_pressed(event):
                    game.draw_screen = rules_screen
                elif game.buttons["start"].button_pressed(event):
                    game.create_client()
                    game.draw_screen = bets_screen
                elif game.buttons["cam"].button_pressed(event):
                    game.cam = not game.cam
                    print("camera", game.cam)
                elif game.buttons["rasp"].button_pressed(event):
                    game.rasp = not game.rasp
                    print("raspberry pi", game.rasp)
                elif game.buttons["link"].button_pressed(event):
                    game.with_linking = not game.with_linking
                    print("face linking", game.with_linking)
                elif game.buttons["exit"].button_pressed(event):
                    game.play_again()
                    return game.players

            # Rules Screen
            elif current_screen == rules_screen:
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_bj

            # Betting Screen
            elif current_screen == bets_screen:
                bal = current_player.balance
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_bj

                for bet_amount, button in game.buttons["bet"]:
                    if button.button_pressed(event) and bal >= bet_amount:
                        current_player.bet = bet_amount
                        current_player.wants_bet = False

            # Playing Screen
            elif current_screen == playing_screen:
                if game.buttons["exit"].button_pressed(event):
                    game.draw_screen = home_screen_bj
                elif game.buttons["hit"].button_pressed(event):
                    game.get_card_func(current_player)
                    current_player.show_cards(screen)
                    current_player.display_score_bj(screen)
                elif current_player.balance >= 2 * current_player.bet and game.buttons["double"].button_pressed(event) \
                        and len(current_player.cards) == 2:
                    current_player.bet = current_player.bet * 2
                    game.get_card_func(current_player)
                    current_player.show_cards(screen)
                    current_player.display_score_bj(screen)
                    current_player.wants_card = False
                elif game.buttons["stand"].button_pressed(event):
                    current_player.wants_card = False

            # Check Results Screen
            elif current_screen == check_results_screen:
                if game.buttons["again"].button_pressed(event):
                    game.play_again()
                    if game.draw_screen != restart_game_screen:
                        game.draw_screen = bets_screen

                elif game.buttons["exit"].button_pressed(event):
                    game.play_again()
                    return game.players

            # Restart Game Screen
            elif current_screen == restart_game_screen:
                game.play_again()
                if game.buttons["restart"].button_pressed(event):
                    game.draw_screen = bets_screen
                    return None
                elif game.buttons["exit"].button_pressed(event):
                    return game.players


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    w, h = pygame.display.get_surface().get_size()
    x_scale, y_scale = w / 1200, h / 600
    pygame.display.set_caption('Virtual Card Game Robot')
    vtk_icon = pygame.image.load('Images/VTK_icon.png')
    pygame.display.set_icon(vtk_icon)

    names = ['Nowa', 'Karel', 'Yannic', 'Jasper']
    players = [Player(name, 10000, i, x_scale, y_scale) for i, name in enumerate(names)]

    playing = True
    while playing:
        game = Blackjack(screen, players, dict(common_buttons, **bj_buttons), x_scale, y_scale)
        remaining_players = blackjack(game)
        if remaining_players is None:
            print("restarting game")
        else:
            playing = False
            print("Game Ended", remaining_players)
