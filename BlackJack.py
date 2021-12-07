from Button import Button, exit_pygame
from Deck import get_random_card_2, load_random_deck
from Player import Player, Library
from AudioPlay import playsound
from time import sleep, perf_counter
from Camera import init_camera, opencv_to_pygame
from mediapipe_pose import linkfacewithhand
import pygame
from gestures_mediapipe import check_all_fingers, check_option, hand_position, LandmarkGetter
import cv2

'''
Bugs: 
- When you exit BlackJack at the Hit or Stand menu and then re-enter BlackJack from MainMenu, the game crashes


To DO:
- Entering starting balance.
- line 348-355(BJ) == line 201-208(BJ) == line 167-173(HL) --> functie van maken.
- ...
'''


# from carddispencer_functies import setup, dcmotor_rotate, servo_rotate , servo_rotate_fromto

def legefunctie():
    print("geef nieuwe kaart")


def legefunctie_2(previous_player, player):
    print("ga van", previous_player, "naar", player)


def legefunctie_3(player):
    print("ga naar", player)


with_rasp = False

if with_rasp:
    give_card = dcmotor_rotate
    rotate_fromto_player = servo_rotate_fromto
    rotate_to = servo_rotate
else:
    give_card = legefunctie
    rotate_fromto_player = legefunctie_2
    rotate_to = legefunctie_3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (31, 171, 57)
RED = (0, 0, 255)

font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)
font_small = pygame.font.SysFont('comicsans', 12)


def get_landmark_list(img, current_player, library, landmarklist, screen, landmarkgetter):
    facedetected_surf = font_small.render('Player Recognized', False, (255, 0, 0))
    notdetected_surf = font_small.render('Player Not Found', False, (255, 0, 0))
    facecoords = library.searchplayer(current_player.name, img)
    templandmarklist = []
    if facecoords:
        screen.blit(facedetected_surf, facedetected_surf.get_rect(topleft=(20, 200)))
    else:
        screen.blit(notdetected_surf, notdetected_surf.get_rect(topleft=(20, 200)))
    for landmark in landmarklist:
        handcoords = hand_position(landmark)
        if facecoords and handcoords:
            img, facecoords, handcoords = face_gest_crop(img, facecoords, handcoords,
                                                         library, current_player, landmarkgetter)
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


def everyone_bust(players):
    everyone_busts = True
    for player in players:
        if player.value_count_bj() != 0:
            everyone_busts = False
    return everyone_busts


def face_gest_crop(img, facecoords, handcoords, library, player, landmarkgetter):
    h, w, c = img.shape
    leftdist = abs(facecoords[0][0] - handcoords[2] * w)
    rightdist = abs(facecoords[0][0] + facecoords[0][2] - handcoords[2] * w)

    if leftdist > rightdist:
        hands = handcoords[2] * w + 150
        if hands > w:
            hands = w
        img = img[:, facecoords[0][0]:int(hands)]
        facecoords = library.searchplayer(player.name, img)
        landmarklist = landmarkgetter(img)
        for landmark in landmarklist:
            handcoords = hand_position(landmark)
    else:
        hands = handcoords[2] * w - 150
        if hands - 150 < 0:
            hands = 0
        img = img[:, int(hands):facecoords[0][0] + facecoords[0][2]]
        facecoords = library.searchplayer(player.name, img)
        landmarklist = landmarkgetter(img)
        for landmark in landmarklist:
            handcoords = hand_position(landmark)
    return img, facecoords, handcoords


def blackjack(screen, clock, library, landmarkgetter, players=None):
    Blackjack_surf = font_big.render('Blackjack', False, BLACK)
    facedetected_surf = font_small.render('Player Recognized', False, (255, 0, 0))
    notdetected_surf = font_small.render('Player Not Found', False, (255, 0, 0))

    deck = load_random_deck()

    if not players:
        player0 = Player('Dealer', 0, 0)
        names = ['Noa', 'Karel', 'Yannic', 'Jasper']
        players = [player0] + [Player(name, 10000, i + 1) for i, name in enumerate(names)]
    else:
        player0 = players.pop(0)

    f = open('blackjackrules.txt', 'r')
    content = f.read()
    f.close()

    game_active = False
    first_card = True

    start_button = Button(BLACK, (550, 480), (100, 65), 'Play!')
    hit_button = Button(BLACK, (330, 250), (110, 60), 'Hit')
    stand_button = Button(BLACK, (770, 250), (110, 60), 'Stand')
    double_button = Button(BLACK, (475, 250), (250, 60), 'Double Down')
    again_button = Button(BLACK, (530, 260), (200, 65), 'Play again!')
    exit_button = Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small')
    rules_button = Button(BLACK, (1140, 560), (40, 20), 'Rules', 'small')
    return_button = Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small')

    bet_buttons = [(i * 1000, Button(BLACK, (325 + i * 75, 350), (50, 30), f'{i}k')) for i in range(1, 6)]

    place_bets = True
    cameracooldown = True
    deal_2_cards = False
    dealer_cards = False
    change_bal = False
    deal_cards = False
    check_results = False
    rules = False
    i, j = 0, 0
    gest_time = 0

    last_fingers = None
    last_option = None
    active_button = None
    selected_button = None

    with_linking = False

    playing_bj = True
    cap = init_camera(0)
    while playing_bj:
        pygame.display.update()
        screen.fill(GREEN)
        if game_active:
            players = list(filter(lambda player: player.balance > 0, players))
            if len(players) == 0:
                game_active = False
            screen.fill(GREEN)

            if perf_counter() - gest_time >= 2:
                cameracooldown = True

            if place_bets:
                if j < len(players):

                    current_player = players[j]

                    if current_player.wants_bet:
                        pygame.draw.rect(screen, GREEN, (0, 0, 1200, 300), 0, -1)
                        current_player.place_bet(screen, bet_buttons)
                        bal = current_player.balance

                        ret, img = cap.read()
                        landmarklist = landmarkgetter(img)

                        if current_player.name in library.libraryembeddings:
                            if with_linking:
                                landmarklist = get_landmark_list(img, current_player, library, landmarklist, screen,
                                                                 landmarkgetter)
                            elif library.searchplayer(current_player.name, img):
                                screen.blit(facedetected_surf, facedetected_surf.get_rect(topleft=(20, 200)))
                            else:
                                screen.blit(notdetected_surf, notdetected_surf.get_rect(topleft=(20, 200)))
                                landmarklist = []

                        if cameracooldown:
                            if landmarklist:
                                amount_fingers, fingername = check_all_fingers(landmarklist[0])
                                cv2.putText(img, fingername, (40, 60), cv2.FONT_HERSHEY_DUPLEX, 2, RED, 4)
                                if amount_fingers:
                                    if bal >= amount_fingers * 1000 and last_fingers == amount_fingers:
                                        current_player.bet = amount_fingers * 1000
                                        current_player.wants_bet = False

                                    elif last_fingers != amount_fingers:
                                        if last_fingers:
                                            last_button = bet_buttons[last_fingers - 1][1]
                                            last_button.set_color(BLACK)
                                            last_button.draw(screen)

                                    active_button = bet_buttons[amount_fingers - 1][1]
                                    active_button.set_color(WHITE)
                                    active_button.draw(screen)

                                last_fingers = amount_fingers
                                pygame.display.update()

                                cameracooldown = False
                                gest_time = perf_counter()

                        for event in pygame.event.get():
                            if exit_button.button_pressed(event):
                                return [player0] + players

                            for bet_amount, button in bet_buttons:
                                if button.button_pressed(event) and bal >= bet_amount:
                                    current_player.bet = bet_amount
                                    current_player.wants_bet = False
                                    active_button = button

                        img = opencv_to_pygame(img)
                        surface = pygame.surfarray.make_surface(img)
                        scale = pygame.transform.rotozoom(surface, -90, 0.25)
                        screen.blit(scale, scale.get_rect(midbottom=(180, 200)))

                    else:
                        last_fingers = None
                        if active_button is not None:
                            active_button.set_color(BLACK)
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
                        deck = get_random_card_2(deck, player)
                        player.show_cards(screen)
                        player.display_score_bj(screen)
                        pygame.display.update()
                        sleep(1)
                        if first_card:
                            rotate_to(player.number)
                            previous_player = player.number
                            give_card()
                            # hier gaat noa zen code moeten schrijven van die kaarten te herkennen en dan pas wordt de tweede kaart gegeven
                            give_card()
                            first_card = False
                        else:
                            if previous_player != player.number:
                                rotate_fromto_player(previous_player, player.number)
                                previous_player = player.number
                            give_card()
                            # hier gaat noa zen code moeten schrijven van die kaarten te herkennen en dan pas wordt de tweede kaart gegeven
                            give_card()

                while len(player0.cards) < 2:
                    if previous_player != 2.5:
                        rotate_fromto_player(previous_player, 2.5)
                        previous_player = 2.5
                    give_card()
                    # hier gaat noa zen code moeten schrijven van die kaarten te herkennen en dan pas wordt de tweede kaart gegeven
                    # de tweede kaart moet voorlopig omgekeerd liggen
                    deck = get_random_card_2(deck, player0)
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
                    if int(current_player.number) != int(previous_player):
                        rotate_fromto_player(previous_player, current_player.number)
                        previous_player = current_player.number
                    if current_player.wants_card:
                        if current_player.value_count_bj() == 'bust':
                            current_player.wants_card = False
                        elif current_player.value_count_bj() == 21:
                            playsound("Sounds/Applause.wav")
                            i += 1
                        else:
                            another_card_surf = font.render(f'{current_player.name}, do you want another card?',
                                                            False, BLACK)
                            screen.blit(another_card_surf, another_card_surf.get_rect(midbottom=(600, 200)))

                            hit_button.draw(screen)
                            stand_button.draw(screen)
                            if double_down := len(current_player.cards) == 2:
                                double_button.draw(screen)

                            ret, img = cap.read()
                            landmarklist = landmarkgetter(img)

                            if current_player.name in library.libraryembeddings:
                                if with_linking:
                                    landmarklist = get_landmark_list(img, current_player, library, landmarklist, screen,
                                                                     landmarkgetter)
                                elif library.searchplayer(current_player.name, img):
                                    screen.blit(facedetected_surf, facedetected_surf.get_rect(topleft=(20, 200)))
                                else:
                                    screen.blit(notdetected_surf, notdetected_surf.get_rect(topleft=(20, 200)))
                                    landmarklist = []

                            if cameracooldown:
                                if landmarklist:
                                    option = check_option(landmarklist[0], double_down)
                                    cv2.putText(img, option, (40, 60), cv2.FONT_HERSHEY_DUPLEX, 2, RED, 4)
                                    if option == "Hit":
                                        if last_option == option:
                                            deck = get_random_card_2(deck, current_player)
                                            current_player.show_cards(screen)
                                            current_player.display_score_bj(screen)
                                            active_button = hit_button
                                        else:
                                            selected_button = hit_button

                                    elif option == "Double Down" and len(current_player.cards) == 2:
                                        if last_option == option:
                                            current_player.bet = current_player.bet * 2
                                            deck = get_random_card_2(deck, current_player)
                                            current_player.show_cards(screen)
                                            current_player.display_score_bj(screen)
                                            current_player.wants_card = False
                                            active_button = double_button
                                        else:
                                            selected_button = double_button

                                    elif option == "Stand":
                                        if last_option == option:
                                            current_player.wants_card = False
                                            active_button = stand_button
                                        else:
                                            selected_button = stand_button

                                    last_option = option
                                    cameracooldown = False
                                    gest_time = perf_counter()

                            if active_button:
                                active_button.set_color(BLACK)
                                active_button.draw(screen)
                                active_button = None
                                selected_button = None
                            elif selected_button:
                                selected_button.set_color(WHITE)
                                selected_button.draw(screen)

                            for event in pygame.event.get():
                                if hit_button.button_pressed(event):
                                    deck = get_random_card_2(deck, current_player)
                                    current_player.show_cards(screen)
                                    current_player.display_score_bj(screen)
                                elif double_button.button_pressed(event):
                                    current_player.bet = current_player.bet * 2
                                    deck = get_random_card_2(deck, current_player)
                                    current_player.show_cards(screen)
                                    current_player.display_score_bj(screen)
                                    current_player.wants_card = False
                                elif stand_button.button_pressed(event):
                                    current_player.wants_card = False
                                elif exit_button.button_pressed(event):
                                    return [player0] + players

                            img = opencv_to_pygame(img)
                            surface = pygame.surfarray.make_surface(img)
                            scale = pygame.transform.rotozoom(surface, -90, 0.25)
                            screen.blit(scale, scale.get_rect(midbottom=(180, 200)))
                    else:
                        last_option = None
                        i += 1
                else:
                    pygame.display.update()
                    sleep(1)
                    if not everyone_bust(players):
                        dealer_cards = True
                    else:
                        deal_cards = False
                        dealer_cards = False
                        change_bal = True
                        check_results = True

            if dealer_cards:
                while 0 < player0.value_count_bj() < 17:
                    player0.show_cards(screen, True)
                    player0.display_score_bj(screen, True)
                    pygame.display.update()
                    sleep(1)
                    # hier moet die ene kaart omgedraaid worden en die worden herkent
                    give_card()
                    # hier gaat noa zen code moeten schrijven van die kaarten te herkennen
                    deck = get_random_card_2(deck, player0)
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
                not_everyone_busts = not everyone_bust(players)
                player0.show_cards(screen, not_everyone_busts)
                player0.display_score_bj(screen, not_everyone_busts)
                again_button.draw(screen)
                for event in pygame.event.get():
                    if again_button.button_pressed(event):
                        last_fingers = None
                        deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players = play_again(players,
                                                                                                              player0)
                    elif exit_button.button_pressed(event):
                        deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players = play_again(players,
                                                                                                              player0)
                        return [player0] + players

            exit_button.draw(screen)

        else:
            screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600, 150)))
            start_button.draw(screen)
            rules_button.draw(screen)
            exit_button.draw(screen)
            H = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Hearts.png"), 0, 0.15)
            S = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Spades.png"), 0, 0.15)
            screen.blit(pygame.transform.rotozoom(H, 10, 1), (510, 250))
            screen.blit(pygame.transform.rotozoom(S, -10, 1), (590, 250))
            if rules:
                pygame.draw.rect(screen, GREEN, (0, 0, 1200, 600))
                pygame.draw.rect(screen, BLACK, (0, 0, 1200, 600), 2, 1)
                return_button.draw(screen)
                split_content = content.splitlines()
                x = 10
                y = 10
                for i, line in enumerate(split_content):
                    rules_surf = font_small.render(line, False, BLACK)
                    screen.blit(rules_surf, rules_surf.get_rect(topleft=(x, y)))
                    y += 12

            for event in pygame.event.get():
                exit_pygame(event)
                if not rules:
                    if start_button.button_pressed(event):
                        game_active = True
                    elif exit_button.button_pressed(event):
                        return [player0] + players
                    elif rules_button.button_pressed(event):
                        rules = True
                elif return_button.button_pressed(event):
                    rules = False

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    blackjack(screen, clock, Library(), LandmarkGetter())
