import pygame
from Button import Button, exit_pygame
from Deck import get_random_card, load_random_deck
from Player import Player, Library
from card_double_detection import get_card
from Camera import init_camera, opencv_to_pygame
from mediapipe_pose import linkfacewithhand
from BlackJack import face_gest_crop
from BlackJack import get_landmark_list
import time
from gestures_mediapipe import *
import cv2
# from carddispencer_functies import setup, dcmotor_rotate, servo_rotate , servo_rotate_fromto

def legefunctie():
    print("geef nieuwe kaart")

with_rasp = False

if with_rasp:
    give_card = dcmotor_rotate
else:
    give_card = legefunctie



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (31, 171, 57)
RED = (0, 0, 255)

font_big = pygame.font.SysFont('comicsans', 80)
font = pygame.font.SysFont('comicsans', 25)
font_small = pygame.font.SysFont('comicsans', 15)

HigherLower_surf = font_big.render('Higher Lower', False, BLACK)
Wrong_surf = font_big.render('Wrong!', False, BLACK)


def get_camera_card(deck, player, screen):
    cap_card = init_camera()
    i = 1
    give_card_again = Button((0, 0, 0), (450, 80), (300, 65), 'Give new card')
    while True:
        if i > 9:
            i = 1
        time.sleep(0.05)
        print("Trying again")
        ret, img = cap_card.read()
        card = get_card(img)
        img = opencv_to_pygame(img)
        surface = pygame.surfarray.make_surface(img)
        scale = pygame.transform.rotozoom(surface, -90, 0.45)
        screen.fill((31, 171, 57))
        screen.blit(scale, scale.get_rect(midbottom=(600, 550)))
        give_card_again.draw(screen)
        for event in pygame.event.get():
            if give_card_again.button_pressed(event):
                print("new card given")
                give_card()

        if card:
            cardname = card.get_rank_suit()
            if cardname in deck:
                deck.remove(cardname)
                player.add_card(card)
                cap_card.release()
                return deck
            else:
                rank, suit = cardname
                if rank == "Joker":
                    surf = font.render("Why so serious? - The Joker", False, (0, 0, 0))
                else:
                    surf = font.render(f"{rank} of {suit} was already seen.", False, (0, 0, 0))
        else:
            surf = font.render("Looking for a card" + "." * (i // 3), False, (0, 0, 0))

        screen.blit(surf, surf.get_rect(midbottom=(600, 50)))
        pygame.display.update()
        i += 1


def last_two_cards(player):
    aantal_kaarten = len(player.cards) - 1

    vorige_kaart = player.cards[aantal_kaarten - 1]
    huidige_kaart = player.cards[aantal_kaarten]

    return vorige_kaart, huidige_kaart


def wrong_guess(player, huidige_kaart, window):
    window.fill((31, 171, 57))
    window.blit(Wrong_surf, Wrong_surf.get_rect(midbottom=(600, 150)))
    player.show_cards(window)
    window.blit(pygame.transform.rotozoom(huidige_kaart.load_image(), 0, 2), (520, 200))
    pygame.display.update()
    time.sleep(3)


def higherlower(screen, clock, players, library, landmarkgetter):
    screen.fill(GREEN)
    deck = load_random_deck()
    player1 = players[1]

    f = open('RulesHigherLower', 'r')
    content = f.read()

    start_button = Button(BLACK, (550, 480), (100, 65), 'Play!')
    again_button = Button(BLACK, (480, 480), (240, 65), 'Play again?')
    high_button = Button(BLACK, (380, 250), (150, 60), 'Higher')
    low_button = Button(BLACK, (680, 250), (150, 60), 'Lower')
    exit_button = Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small')
    rules_exit_button = Button(BLACK, (1140, 20), (40, 20), 'Exit', 'small')
    rules_button = Button(BLACK, (1140, 560), (40, 20), 'Rules', 'small')

    facedetected_surf = font_small.render('Player Recognized', False, (255, 0, 0))
    notdetected_surf = font_small.render('Player Not Found', False, (255, 0, 0))

    game_active = False
    high = False
    low = False
    lost = False
    rules = False

    with_camera = False
    with_linking = False
    gest_time = 0
    cameracooldown = True

    lastindex = None
    active_button = None
    selected_button = None

    if with_camera:
        get_card_func = get_camera_card
    else:
        get_card_func = get_random_card
    cap = init_camera(0)
    while True:
        pygame.display.update()
        if game_active:
            if not lost:
                screen.fill(GREEN)
                player1.show_name(screen)
                player1.display_score_hl(screen)

                if len(player1.cards) < 1:
                    give_card()
                    deck = get_card_func(deck, player1, screen)

                player1.show_cards(screen)
                pick_higher_lower_surf = font.render(
                    f'{player1.name}, is the next card going to be higher or lower?', False, BLACK)
                screen.blit(pick_higher_lower_surf, pick_higher_lower_surf.get_rect(midbottom=(600, 200)))

                high_button.draw(screen)
                low_button.draw(screen)

                ret, img = cap.read()
                landmarklist = landmarkgetter(img)

                if time.perf_counter() - gest_time >= 2:
                    cameracooldown = True

                if player1.name in library.libraryembeddings:
                    if with_linking:
                        landmarklist = get_landmark_list(img, player1, library, landmarklist, screen, landmarkgetter)
                    elif library.searchplayer(player1.name, img):
                        screen.blit(facedetected_surf, facedetected_surf.get_rect(topleft=(20, 200)))
                    else:
                        screen.blit(notdetected_surf, notdetected_surf.get_rect(topleft=(20, 200)))
                        landmarklist = []

                if cameracooldown:
                    if landmarklist:
                        index = check_index(landmarklist[0])
                        cv2.putText(img, index, (40, 60), cv2.FONT_HERSHEY_DUPLEX, 2, RED, 4)
                        if index == "Index Up":
                            if lastindex == index:
                                deck = get_card_func(deck, player1, screen)
                                player1.show_cards(screen)
                                vorige, huidige = last_two_cards(player1)
                                high = index_up(landmarklist[0]) and vorige.hl_value > huidige.hl_value
                                active_button = high_button
                            else:
                                selected_button = high_button
                        elif index == "Index Down":
                            if lastindex == index:
                                deck = get_card_func(deck, player1, screen)
                                player1.show_cards(screen)
                                vorige, huidige = last_two_cards(player1)
                                low = index_down(landmarklist[0]) and vorige.hl_value < huidige.hl_value
                                active_button = low_button
                            else:
                                selected_button = low_button

                        lastindex = index
                        cameracooldown = False
                        gest_time = time.perf_counter()

                if active_button:  # If a button is "pressed"
                    active_button.set_color((255, 0, 0))
                    active_button.draw(screen)
                    pygame.display.update()
                    time.sleep(0.5)
                    active_button = None
                    selected_button = None
                elif selected_button:  # This shows what button this gesture WOULD press
                    selected_button.set_color(WHITE)
                    selected_button.draw(screen)

                for event in pygame.event.get():
                    pygame.display.update()
                    if high_button.button_pressed(event) or low_button.button_pressed(event):
                        give_card()
                        deck = get_card_func(deck, player1, screen)
                        player1.show_cards(screen)
                        vorige, huidige = last_two_cards(player1)
                        high = high_button.button_pressed(event) and vorige.hl_value > huidige.hl_value
                        low = low_button.button_pressed(event) and vorige.hl_value < huidige.hl_value

                high_button.set_color(BLACK)
                low_button.set_color(BLACK)

                img = opencv_to_pygame(img)
                surface = pygame.surfarray.make_surface(img)
                scale = pygame.transform.rotozoom(surface, -90, 0.25)
                screen.blit(scale, scale.get_rect(midbottom=(180, 200)))

                if high or low:
                    lost = True
                    pygame.display.update()
                    wrong_guess(player1, huidige, screen)

            else:
                screen.fill(GREEN)
                again_button.draw(screen)
                exit_button.draw(screen)

                for event in pygame.event.get():
                    if again_button.button_pressed(event):
                        player1.cards = []
                        deck = load_random_deck()
                        lost = False
                        high = False
                        low = False
                    if exit_button.button_pressed(event):
                        player1.cards = []
                        return players

        else:
            screen.fill(GREEN)
            screen.blit(HigherLower_surf, HigherLower_surf.get_rect(midbottom=(600, 150)))
            start_button.draw(screen)
            rules_button.draw(screen)
            exit_button.draw(screen)

            if rules:
                pygame.draw.rect(screen, GREEN, (0, 0, 1200, 600))
                pygame.draw.rect(screen, BLACK, (0, 0, 1200, 600), 2, 1)
                rules_exit_button.draw(screen)
                splittedcontent = content.splitlines()
                x = 10
                y = 10
                for i, line in enumerate(splittedcontent):
                    rules_surf = font.render(line, False, BLACK)
                    screen.blit(rules_surf, rules_surf.get_rect(topleft=(x, y)))
                    y += 30

            for event in pygame.event.get():
                exit_pygame(event)
                if not rules:
                    if rules_button.button_pressed(event):
                        rules = True
                    if start_button.button_pressed(event):
                        game_active = True
                    elif exit_button.button_pressed(event):
                        return players
                elif rules_exit_button.button_pressed(event):
                    rules = False

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    higherlower(screen, clock, [0, Player('Matthias', 10000, 1)], Library(), LandmarkGetter())
