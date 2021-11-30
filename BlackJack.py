from Button import Button, button_pressed, exit_pygame
from Deck import load_deck, get_random_card, load_random_deck
from Player import Player
from AudioPlay import playsound
from time import sleep
from Camera import init_camera
from mediapipe_pose import linkfacewithhand
from Button import turn_white
import time
import pygame
from gestures_mediapipe_class import gesture_recognition

'''
Bugs: 

To DO:
- Entering player names and amount of players.
- Entering starting balance.
- If BlackJack 3:2 payment.
- ...
'''


def play_again(players, player0):
    deal_2_cards = False
    deal_cards = False
    check_results = False
    place_bets = True
    i = 0
    j = 0
    for player in players:
        player.cards = None
        player.wants_bet = True
        player.wants_card = False
    player0.cards = None
    deck = load_random_deck()
    return deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players


def camera_button(pressed_button, buttonlist, fingerlist):
    for idx, buttonoptions in enumerate(buttonlist):
        if pressed_button == buttonoptions:
            for idx2, finger in enumerate(fingerlist):
                if finger != fingerlist[idx]:
                    fingerlist[idx2] = False
                else:
                    fingerlist[idx2] = True
            for button in buttonlist:
                if button != pressed_button:
                    button.set_color((0, 0, 0))
                else:
                    button.set_color((255, 255, 255))
    return fingerlist


def blackjack(screen, clock, library, players=[]):
    test_font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
    test_font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)
    test_font_small = pygame.font.SysFont('comicsans', 12)

    Blackjack_surf = test_font_big.render('Blackjack', False, (0, 0, 0))
    f = open('blackjackrules.txt', 'r')
    content = f.read()

    deck = load_random_deck()

    if players == []:
        player0 = Player('Dealer', 0, 0)
        names = ['Matthias', 'Karel', 'Yannic', 'Jasper']
        players = [player0] + [Player(name, 10000, i + 1) for i, name in enumerate(names)]
    else:
        print(players)
        player0 = players.pop(0)

    game_active = False

    start_button = Button((0, 0, 0), (550, 480), (100, 65), 'Play!')
    yes_button = Button((0, 0, 0), (330, 250), (110, 60), 'Hit')
    no_button = Button((0, 0, 0), (770, 250), (110, 60), 'Stand')
    double_button = Button((0, 0, 0), (475, 250), (250, 60), 'Double Down')
    again_button = Button((0, 0, 0), (530, 260), (200, 65), 'Play again!')
    exit_button = Button((0, 0, 0), (1140, 20), (40, 20), 'Exit', 'small')
    rules_button = Button((0, 0, 0), (1140, 560), (40, 20), 'Rules', 'small')
    onek_button = Button((0, 0, 0), (325 + 1 * 75, 350), (50, 30), f'1k')
    twok_button = Button((0, 0, 0), (325 + 2 * 75, 350), (50, 30), f'2k')
    threek_button = Button((0, 0, 0), (325 + 3 * 75, 350), (50, 30), f'3k')
    fourk_button = Button((0, 0, 0), (325 + 4 * 75, 350), (50, 30), f'4k')
    fivek_button = Button((0, 0, 0), (325 + 5 * 75, 350), (50, 30), f'5k')
    kbuttonlist = [onek_button, twok_button, threek_button, fourk_button, fivek_button]
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

    one_finger = False
    two_finger = False
    three_finger = False
    four_finger = False
    five_finger = False
    fingerlist = [one_finger, two_finger, three_finger, four_finger, five_finger]
    hit_clicked = False
    doubledown_clicked = False
    stand_clicked = False
    clickedlist = [hit_clicked, doubledown_clicked, stand_clicked]

    playing_bj = True
    cap = init_camera(0)
    while playing_bj:

        pygame.display.update()

        if game_active:

            if len(players) == 0:
                game_active = False
            screen.fill((31, 171, 57))

            if time.perf_counter() - gest_time >= 2:
                cameracooldown = True

            if place_bets:
                if j < len(players):
                    for player in players:
                        if player.balance == 0:
                            players.remove(player)
                    if players[j].wants_bet:
                        pygame.draw.rect(screen, (31, 171, 57), (0, 0, 1200, 300), 0, -1)
                        bal = players[j].balance
                        players[j].bet = 0
                        question_surf = players[j].font_big.render(f'{players[j].name}, how much do you want to bet?',
                                                                   False,
                                                                   (10, 10, 10))
                        screen.blit(question_surf, question_surf.get_rect(midbottom=(600, 250)))
                        bet_buttons = [(1000, onek_button), (2000, twok_button), (3000, threek_button),
                                       (4000, fourk_button), (5000, fivek_button)]
                        for bet_amount, button in bet_buttons:
                            if bal >= bet_amount:
                                button.draw(screen)

                        ret, img = cap.read()
                        gest_rec = gesture_recognition()
                        landmarklist = gest_rec.get_landmarks(img)

                        if players[j].name in library.libraryembeddings:
                            facecoords = library.searchplayer(players[j].name, img)
                            templandmarklist = []
                            for landmark in landmarklist:
                                handcoords = gest_rec.hand_position(landmark)
                                if len(facecoords) > 0 and len(handcoords) > 0:
                                    img, bool = linkfacewithhand(img, facecoords[0], handcoords)
                                    if bool:
                                        templandmarklist.append(landmark)
                            landmarklist = templandmarklist

                        if cameracooldown:
                            if len(landmarklist) > 0 and (gest_rec.index_up(img, landmarklist[0])):
                                if bal >= 1000 and one_finger:
                                    players[j].bet = 1000
                                    one_finger = False
                                [one_finger, two_finger, three_finger, four_finger, five_finger] = camera_button(
                                    onek_button, kbuttonlist, fingerlist)
                                onek_button.draw(screen)
                                cameracooldown = False
                                gest_time = time.perf_counter()
                            elif len(landmarklist) > 0 and (gest_rec.fingers_two(img, landmarklist[0])):
                                if bal >= 2000 and two_finger:
                                    players[j].bet = 2000
                                    two_finger = False
                                [one_finger, two_finger, three_finger, four_finger, five_finger] = camera_button(
                                    twok_button, kbuttonlist, fingerlist)
                                twok_button.draw(screen)
                                cameracooldown = False
                                gest_time = time.perf_counter()
                            elif len(landmarklist) > 0 and (gest_rec.fingers_three(img, landmarklist[0])):
                                if bal >= 3000 and three_finger:
                                    players[j].bet = 3000
                                    three_finger = False
                                [one_finger, two_finger, three_finger, four_finger, five_finger] = camera_button(
                                    threek_button, kbuttonlist, fingerlist)
                                threek_button.draw(screen)
                                cameracooldown = False
                                gest_time = time.perf_counter()
                            elif len(landmarklist) > 0 and (gest_rec.fingers_four(img, landmarklist[0])):
                                if bal >= 4000 and four_finger:
                                    players[j].bet = 4000
                                    four_finger = False
                                [one_finger, two_finger, three_finger, four_finger, five_finger] = camera_button(
                                    fourk_button, kbuttonlist, fingerlist)
                                fourk_button.draw(screen)
                                cameracooldown = False
                                gest_time = time.perf_counter()
                            elif len(landmarklist) > 0 and (gest_rec.fingers_five(img, landmarklist[0])):
                                if bal >= 5000 and five_finger:
                                    players[j].bet = 5000
                                    five_finger = False
                                [one_finger, two_finger, three_finger, four_finger, five_finger] = camera_button(
                                    fivek_button, kbuttonlist, fingerlist)
                                fivek_button.draw(screen)
                                cameracooldown = False
                                gest_time = time.perf_counter()

                        for event in pygame.event.get():
                            if button_pressed(exit_button, event):
                                players_incl = [player0]
                                for player in players:
                                    players_incl.append(player)
                                return players_incl

                            if button_pressed(onek_button, event) and bal >= 1000:
                                players[j].bet = 1000
                            elif button_pressed(twok_button, event) and bal >= 2000:
                                players[j].bet = 2000
                            elif button_pressed(threek_button, event) and bal >= 3000:
                                players[j].bet = 3000
                            elif button_pressed(fourk_button, event) and bal >= 4000:
                                players[j].bet = 4000
                            elif button_pressed(fivek_button, event) and bal >= 5000:
                                players[j].bet = 5000
                    if players[j].bet != 0:
                        players[j].wants_bet = False
                    if not players[j].wants_bet:
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
                    if player.cards is None:
                        player.cards = []
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

                if player0.cards is None:
                    player0.cards = []
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
                    if players[i].wants_card:
                        if players[i].value_count_bj() == 'bust':
                            players[i].wants_card = False
                        if players[i].value_count_bj() == 21:
                            playsound("Sounds/Applause.wav")
                            i += 1
                        else:
                            another_card_surf = test_font.render(players[i].name + ', do you want another card?',
                                                                 False, (0, 0, 0))
                            screen.blit(another_card_surf, another_card_surf.get_rect(midbottom=(600, 200)))
                            yes_button.draw(screen)
                            no_button.draw(screen)

                            ret, img = cap.read()
                            gest_rec = gesture_recognition()
                            landmarklist = gest_rec.get_landmarks(img)

                            if players[i].name in library.libraryembeddings:
                                facecoords = library.searchplayer(players[i].name, img)
                                templandmarklist = []
                                for landmark in landmarklist:
                                    handcoords = gest_rec.hand_position(landmark)
                                    if len(facecoords) > 0 and len(handcoords) > 0:
                                        img, bool = linkfacewithhand(img, facecoords[0], handcoords)
                                        if bool:
                                            templandmarklist.append(landmark)
                                landmarklist = templandmarklist

                            if len(players[i].cards) == 2:
                                double_button.draw(screen)
                                if cameracooldown:
                                    if len(landmarklist) > 0 and (gest_rec.index_up(img, landmarklist[0])):
                                        if hit_clicked:
                                            deck = get_random_card(deck, players[i], screen)
                                            players[i].show_cards(screen)
                                            players[i].display_score_bj(screen)
                                            hit_clicked = False
                                        [hit_clicked, doubledown_clicked, stand_clicked] = camera_button(yes_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        yes_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif len(landmarklist) > 0 and (gest_rec.fingers_five(img, landmarklist[0])):
                                        if stand_clicked:
                                            players[i].wants_card = False
                                            stand_clicked = False
                                        [hit_clicked, doubledown_clicked, stand_clicked] = camera_button(no_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        no_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif len(landmarklist) > 0 and (gest_rec.fingers_two(img, landmarklist[0])):
                                        if doubledown_clicked:
                                            players[i].bet = players[i].bet * 2
                                            deck = get_random_card(deck, players[i], screen)
                                            players[i].show_cards(screen)
                                            players[i].display_score_bj(screen)
                                            players[i].wants_card = False
                                            doubledown_clicked = False
                                        [hit_clicked, doubledown_clicked, stand_clicked] = camera_button(
                                            doubledown_clicked, optionbuttonlist, clickedlist)
                                        double_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                for event in pygame.event.get():
                                    if button_pressed(yes_button, event):
                                        deck = get_random_card(deck, players[i], screen)
                                        players[i].show_cards(screen)
                                        players[i].display_score_bj(screen)
                                    elif button_pressed(no_button, event):
                                        players[i].wants_card = False
                                    elif button_pressed(double_button, event):
                                        players[i].bet = players[i].bet * 2
                                        deck = get_random_card(deck, players[i], screen)
                                        players[i].show_cards(screen)
                                        players[i].display_score_bj(screen)
                                        players[i].wants_card = False
                                    elif button_pressed(exit_button, event):
                                        players_incl = [player0]
                                        for player in players:
                                            players_incl.append(player)
                                        return players_incl
                            else:
                                if cameracooldown:
                                    if len(landmarklist) > 0 and (gest_rec.index_up(img, landmarklist[0])):
                                        if hit_clicked:
                                            deck = get_random_card(deck, players[i], screen)
                                            players[i].show_cards(screen)
                                            players[i].display_score_bj(screen)
                                            hit_clicked = False
                                        [hit_clicked, doubledown_clicked, stand_clicked] = camera_button(yes_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        yes_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif len(landmarklist) > 0 and (gest_rec.fingers_five(img, landmarklist[0])):
                                        if stand_clicked:
                                            players[i].wants_card = False
                                            stand_clicked = False
                                        [hit_clicked, doubledown_clicked, stand_clicked] = camera_button(no_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        no_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                    elif len(landmarklist) > 0 and (gest_rec.fingers_two(img, landmarklist[0])):
                                        if doubledown_clicked:
                                            players[i].bet = players[i].bet * 2
                                            deck = get_random_card(deck, players[i], screen)
                                            players[i].show_cards(screen)
                                            players[i].display_score_bj(screen)
                                            players[i].wants_card = False
                                            doubledown_clicked = False
                                        [hit_clicked, doubledown_clicked, stand_clicked] = camera_button(double_button,
                                                                                                         optionbuttonlist,
                                                                                                         clickedlist)
                                        yes_button.draw(screen)
                                        cameracooldown = False
                                        gest_time = time.perf_counter()
                                for event in pygame.event.get():
                                    if button_pressed(yes_button, event):
                                        deck = get_random_card(deck, players[i], screen)
                                        players[i].show_cards(screen)
                                        players[i].display_score_bj(screen)
                                    elif button_pressed(no_button, event):
                                        players[i].wants_card = False
                                    elif button_pressed(exit_button, event):
                                        players_incl = [player0]
                                        for player in players:
                                            players_incl.append(player)
                                        return players_incl
                        if i >= len(players):
                            pass
                        else:
                            if not players[i].wants_card:
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
                pygame.draw.rect(screen, (31, 171, 57), (0, 360, 1200, 25), 0)
                if dealer_score == 21 and len(player0.cards) == 2:
                    dealer_blackjack = True
                for player in players:
                    player.display_results(screen, dealer_score, 'bj', dealer_blackjack)
                player0.show_cards(screen, True)
                player0.display_score_bj(screen, True)
                again_button.draw(screen)
                for event in pygame.event.get():
                    if button_pressed(again_button, event):
                        one_finger = False
                        two_finger = False
                        three_finger = False
                        four_finger = False
                        five_finger = False
                        hit_clicked = False
                        doubledown_clicked = False
                        stand_clicked = False
                        deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players = play_again(players, player0)
                    elif button_pressed(exit_button, event):
                        deal_2_cards, deal_cards, check_results, place_bets, i, j, deck, players = play_again(players, player0)
                        players_incl = [player0]
                        for player in players:
                            players_incl.append(player)
                        return players_incl

            exit_button.draw(screen)

        else:
            screen.fill((31, 171, 57))
            screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600, 150)))
            start_button.draw(screen)
            rules_button.draw(screen)
            H = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Hearts.png"), 0, 0.15)
            S = pygame.transform.rotozoom(pygame.image.load(f"Images/Cards/Ace_Spades.png"), 0, 0.15)
            screen.blit(pygame.transform.rotozoom(H, 10, 1), (510, 250))
            screen.blit(pygame.transform.rotozoom(S, -10, 1), (590, 250))
            if rules:
                pygame.draw.rect(screen, (31, 171, 57), (0, 0, 1200, 600))
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1200, 600), 2, 1)
                exit_button.draw(screen)
                splittedcontent = content.splitlines()
                x = 10
                y = 10
                for i, line in enumerate(splittedcontent):
                    rules_surf = test_font_small.render(line, False, (0, 0, 0))
                    screen.blit(rules_surf, rules_surf.get_rect(topleft=(x, y)))
                    y += 12

            for event in pygame.event.get():
                exit_pygame(event)
                if button_pressed(start_button, event):
                    game_active = True
                if not rules:
                    if button_pressed(rules_button, event):
                        rules = True
                elif button_pressed(exit_button, event):
                    rules = False

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    blackjack(screen, clock)
