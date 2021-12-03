from Button import Button, exit_pygame
from Deck import get_random_card, load_random_deck
from Player import Player, Library
from AudioPlay import playsound
from time import sleep
from Camera import init_camera, opencv_to_pygame
from mediapipe_pose import linkfacewithhand
from math import sqrt
import time
import pygame
import cv2
from gestures_mediapipe import *

'''
Bugs: 

To DO:
- Entering starting balance.
- If BlackJack 3:2 payment.
- ...
'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (31, 171, 57)

test_font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
test_font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)
test_font_small = pygame.font.SysFont('comicsans', 12)


def get_landmark_list(img, current_player, library, landmarklist, screen):
    facedetected_surf = test_font_small.render('Player Recognized', False, (255, 0, 0))
    notdetected_surf = test_font_small.render('Player Not Found', False, (255, 0, 0))
    facecoords = library.searchplayer(current_player.name, img)
    templandmarklist = []
    if facecoords:
        screen.blit(facedetected_surf, facedetected_surf.get_rect(topleft=(10, 10)))
    else:
        screen.blit(notdetected_surf, notdetected_surf.get_rect(topleft=(10, 10)))
    for landmark in landmarklist:
        handcoords = hand_position(landmark)
        if facecoords and handcoords:
            img, facecoords, handcoords = face_gest_crop(img, facecoords, handcoords,
                                                         library, current_player)
            bool = False
            if facecoords:
                img, bool = linkfacewithhand(img, facecoords[0], handcoords)
            if bool:
                templandmarklist.append(landmark)
    return templandmarklist


def play_again(players, player0):
    deal_2_cards = False
    deal_cards = False
    check_results = False
    place_bets = True
    i = 0
    j = 0
    for player in players:
        player.cards = []
        player.wants_bet = True
        player.wants_card = False
    player0.cards = []
    deck = load_random_deck()
    return deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players


def camera_button(pressed_button, buttonlist, fingerlist):
    for idx, button in enumerate(buttonlist):
        if pressed_button == button:
            button.set_color(WHITE)
            for idx2, finger in enumerate(fingerlist):
                if idx2 != idx:
                    fingerlist[idx2] = False
                else:
                    fingerlist[idx2] = True
        else:
            button.set_color(BLACK)
    return fingerlist


def face_gest_crop(img, facecoords, handcoords, library, player):
    h, w, c = img.shape
    (leftdist, rightdist) = (sqrt((facecoords[0][0] - handcoords[2] * w) ** 2),
                             sqrt((facecoords[0][0] + facecoords[0][2] - handcoords[2] * w) ** 2))
    # TODO is dit voor de absolute waarde? want kan je dan niet beter abs doen
    if leftdist > rightdist:
        hands = handcoords[2] * w + 150
        if hands > w:
            hands = w
        img = img[:, facecoords[0][0]:int(hands)]
        facecoords = library.searchplayer(player.name, img)
        landmarklist = get_landmarks(img)
        for landmark in landmarklist:
            handcoords = hand_position(landmark)
    else:
        hands = handcoords[2] * w - 150
        if hands - 150 < 0:
            hands = 0
        img = img[:, int(hands):facecoords[0][0] + facecoords[0][2]]
        facecoords = library.searchplayer(player.name, img)
        landmarklist = get_landmarks(img)
        for landmark in landmarklist:
            handcoords = hand_position(landmark)
    return img, facecoords, handcoords


def blackjack(screen, clock, library, players=None):
    Blackjack_surf = test_font_big.render('Blackjack', False, BLACK)

    deck = load_random_deck()

    if not players:
        player0 = Player('Dealer', 0, 0)
        names = ['Noa', 'Karel', 'Yannic', 'Jasper']
        players = [player0] + [Player(name, 10000, i + 1) for i, name in enumerate(names)]
    else:
        player0 = players.pop(0)

    game_active = False

    start_button = Button(BLACK, (550, 480), (100, 65), 'Play!')
    yes_button = Button(BLACK, (330, 250), (110, 60), 'Hit')
    no_button = Button(BLACK, (770, 250), (110, 60), 'Stand')
    double_button = Button(BLACK, (475, 250), (250, 60), 'Double Down')
    again_button = Button(BLACK, (530, 260), (200, 65), 'Play again!')
    exit_button = Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small')
    rules_button = Button(BLACK, (1140, 560), (40, 20), 'Rules', 'small')

    bet_buttons = [(i * 1000, Button(BLACK, (325 + i * 75, 350), (50, 30), f'{i}k')) for i in range(1, 6)]

    optionbuttonlist = [yes_button, no_button, double_button]

    place_bets = True
    cameracooldown = True
    deal_2_cards = False
    dealer_cards = False
    change_bal = False
    deal_cards = False
    check_results = False
    rules = False
    i = 0
    j = 0
    gest_time = 0

    last_fingers = None

    hit_clicked = False
    doubledown_clicked = False
    stand_clicked = False
    clickedlist = [hit_clicked, stand_clicked, doubledown_clicked]

    playing_bj = True
    cap = init_camera(0)
    while playing_bj:

        pygame.display.update()

        if game_active:
            players = list(filter(lambda player: player.balance > 0, players))
            if len(players) == 0:
                game_active = False
            screen.fill(GREEN)

            if time.perf_counter() - gest_time >= 2:
                cameracooldown = True

            if place_bets:
                if j < len(players):

                    current_player = players[j]

                    if current_player.wants_bet:
                        pygame.draw.rect(screen, GREEN, (0, 0, 1200, 300), 0, -1)
                        current_player.place_bet(screen, bet_buttons)
                        bal = current_player.balance

                        ret, img = cap.read()
                        landmarklist = get_landmarks(img)

                        if current_player.name in library.libraryembeddings:
                            landmarklist = get_landmark_list(img, current_player, library, landmarklist, screen)

                        if cameracooldown:
                            if landmarklist:
                                amount_fingers, img = check_all_fingers(landmarklist[0])
                                if amount_fingers:
                                    if bal >= amount_fingers * 1000 and last_fingers == amount_fingers:
                                        current_player.bet = amount_fingers * 1000
                                        current_player.wants_bet = False

                                    elif last_fingers != amount_fingers:
                                        if last_fingers:
                                            last_button = bet_buttons[last_fingers - 1][1]
                                            last_button.set_color(BLACK)
                                            last_button.draw(screen)

                                    current_button = bet_buttons[amount_fingers - 1][1]
                                    current_button.set_color(WHITE)
                                    current_button.draw(screen)

                                last_fingers = amount_fingers
                                pygame.display.update()

                            cameracooldown = False
                            gest_time = time.perf_counter()

                        for event in pygame.event.get():
                            if exit_button.button_pressed(event):
                                return [player0] + players

                            for bet_amount, button in bet_buttons:
                                if button.button_pressed(event) and bal >= bet_amount:
                                    current_player.bet = bet_amount
                                    current_player.wants_bet = False
                                    current_button = button

                        img = opencv_to_pygame(img)
                        surface = pygame.surfarray.make_surface(img)
                        scale = pygame.transform.rotozoom(surface, -90, 0.25)
                        screen.blit(scale, scale.get_rect(midbottom=(180, 200)))

                    if not current_player.wants_bet:
                        last_fingers = None
                        current_button.set_color(BLACK)
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

                    while len(player.cards) < 2:
                        deck = get_random_card(deck, player, screen)
                        player.show_cards(screen)
                        player.display_score_bj(screen)
                        pygame.display.update()
                        sleep(1)
                        deck = get_random_card(deck, player, screen)
                for player in players:
                    player.show_cards(screen)
                    player.display_score_bj(screen)
                    pygame.display.update()
                    sleep(1)


                while len(player0.cards) < 2:
                    deck = get_random_card(deck, player0, screen)
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
                    current_player = players[i]
                    if current_player.wants_card:
                        if current_player.value_count_bj() == 'bust':
                            current_player.wants_card = False
                        if current_player.value_count_bj() == 21:
                            playsound("Sounds/Applause.wav")
                            i += 1
                        else:
                            another_card_surf = test_font.render(f'{current_player.name}, do you want another card?',
                                                                 False, BLACK)
                            screen.blit(another_card_surf, another_card_surf.get_rect(midbottom=(600, 200)))
                            yes_button.draw(screen)
                            no_button.draw(screen)

                            ret, img = cap.read()
                            landmarklist = get_landmarks(img)

                            if current_player.name in library.libraryembeddings:
                                landmarklist = get_landmark_list(img, current_player, library, landmarklist, screen)

                            if len(current_player.cards) == 2:
                                double_button.draw(screen)
                                if cameracooldown:
                                    if landmarklist and index_up(img, landmarklist[0]):
                                        if hit_clicked:
                                            deck = get_random_card(deck, current_player, screen)
                                            current_player.show_cards(screen)
                                            current_player.display_score_bj(screen)

                                        [hit_clicked, stand_clicked, doubledown_clicked] = camera_button(yes_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        yes_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif landmarklist and fingers_five(img, landmarklist[0]):
                                        if stand_clicked:
                                            current_player.wants_card = False

                                        [hit_clicked, stand_clicked, doubledown_clicked] = camera_button(
                                            no_button, optionbuttonlist, clickedlist)
                                        no_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif landmarklist and fingers_two(img, landmarklist[0]):
                                        if doubledown_clicked:
                                            current_player.bet = current_player.bet * 2
                                            deck = get_random_card(deck, current_player, screen)
                                            current_player.show_cards(screen)
                                            current_player.display_score_bj(screen)
                                            current_player.wants_card = False

                                        [hit_clicked, stand_clicked, doubledown_clicked] = camera_button(
                                            double_button, optionbuttonlist, clickedlist)
                                        double_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                for event in pygame.event.get():
                                    if yes_button.button_pressed(event):
                                        deck = get_random_card(deck, current_player, screen)
                                        current_player.show_cards(screen)
                                        current_player.display_score_bj(screen)
                                    elif no_button.button_pressed(event):
                                        current_player.wants_card = False
                                    elif double_button.button_pressed(event):
                                        current_player.bet = current_player.bet * 2
                                        deck = get_random_card(deck, current_player, screen)
                                        current_player.show_cards(screen)
                                        current_player.display_score_bj(screen)
                                        current_player.wants_card = False
                                    elif exit_button.button_pressed(event):
                                        return [player0] + players
                            else:
                                if cameracooldown:
                                    if landmarklist and index_up(img, landmarklist[0]):
                                        if hit_clicked:
                                            deck = get_random_card(deck, current_player, screen)
                                            current_player.show_cards(screen)
                                            current_player.display_score_bj(screen)

                                        [hit_clicked, stand_clicked, doubledown_clicked] = camera_button(yes_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        yes_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif landmarklist and fingers_five(img, landmarklist[0]):
                                        if stand_clicked:
                                            current_player.wants_card = False

                                        [hit_clicked, stand_clicked, doubledown_clicked] = camera_button(no_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        no_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                for event in pygame.event.get():
                                    if yes_button.button_pressed(event):
                                        deck = get_random_card(deck, current_player, screen)
                                        current_player.show_cards(screen)
                                        current_player.display_score_bj(screen)
                                    elif no_button.button_pressed(event):
                                        current_player.wants_card = False
                                    elif exit_button.button_pressed(event):
                                        return [player0] + players
                        if i >= len(players):
                            pass
                        else:
                            if not current_player.wants_card:
                                i += 1
                else:
                    pygame.display.update()
                    sleep(1)
                    dealer_cards = True

            if dealer_cards:
                while 0 < player0.value_count_bj() < 17:
                    player0.show_cards(screen, True)
                    player0.display_score_bj(screen, True)
                    pygame.display.update()
                    sleep(1)
                    deck = get_random_card(deck, player0, screen)
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
                pygame.draw.rect(screen, GREEN, (0, 360, 1200, 25), 0)
                if dealer_score == 21 and len(player0.cards) == 2:
                    dealer_blackjack = True
                for player in players:
                    player.display_results(screen, dealer_score, 'bj', dealer_blackjack)
                player0.show_cards(screen, True)
                player0.display_score_bj(screen, True)
                again_button.draw(screen)
                for event in pygame.event.get():
                    if again_button.button_pressed(event):
                        last_fingers = None
                        hit_clicked = False
                        doubledown_clicked = False
                        stand_clicked = False
                        deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players = play_again(players,
                                                                                                              player0)
                    elif exit_button.button_pressed(event):
                        deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players = play_again(players,
                                                                                                              player0)
                        return [player0] + players

            exit_button.draw(screen)

        else:
            screen.fill(GREEN)
            screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600, 150)))
            start_button.draw(screen)
            rules_button.draw(screen)
            H = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Hearts.png"), 0, 0.15)
            S = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Spades.png"), 0, 0.15)
            screen.blit(pygame.transform.rotozoom(H, 10, 1), (510, 250))
            screen.blit(pygame.transform.rotozoom(S, -10, 1), (590, 250))
            if rules:
                pygame.draw.rect(screen, GREEN, (0, 0, 1200, 600))
                pygame.draw.rect(screen, BLACK, (0, 0, 1200, 600), 2, 1)
                exit_button.draw(screen)
                f = open('blackjackrules.txt', 'r')
                content = f.read()
                splittedcontent = content.splitlines()
                x = 10
                y = 10
                for i, line in enumerate(splittedcontent):
                    rules_surf = test_font_small.render(line, False, BLACK)
                    screen.blit(rules_surf, rules_surf.get_rect(topleft=(x, y)))
                    y += 12
                f.close()

            for event in pygame.event.get():
                exit_pygame(event)
                if start_button.button_pressed(event):
                    game_active = True
                if not rules:
                    if rules_button.button_pressed(event):
                        rules = True
                elif exit_button.button_pressed(event):
                    rules = False

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    blackjack(screen, clock, Library())
