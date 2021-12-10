import cv2
from time import sleep
from Button import Button
from card_double_detection import get_card
import pygame

BLACK = (0, 0, 0)
GREEN = (31, 171, 57)
font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)


def init_camera(source=1):
    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    return cap


def opencv_to_pygame(img):
    img = cv2.flip(img, 1, img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def get_camera_card(game, player):
    screen = game.screen
    cap_card = init_camera()
    i = 1
    give_card_again = Button(BLACK, (450, 80), (300, 65), 'Give new card')
    while True:
        if i > 9:
            i = 1
        sleep(0.05)
        # print("Trying again")
        ret, img = cap_card.read()
        card = get_card(img)
        img = opencv_to_pygame(img)
        surface = pygame.surfarray.make_surface(img)
        scale = pygame.transform.rotozoom(surface, -90, 0.45)
        screen.fill(GREEN)
        screen.blit(scale, scale.get_rect(midbottom=(600, 550)))
        give_card_again.draw(screen)
        for event in pygame.event.get():
            if give_card_again.button_pressed(event):
                print("new card given")
                game.give_card()

        if card:
            cardname = card.get_rank_suit()
            if cardname in game.deck:
                print(f"{player.name} got {cardname[0]} of {cardname[1]}")
                game.deck.remove(cardname)
                player.add_card(card)
                cap_card.release()
                break
            else:
                rank, suit = cardname
                if rank == "Joker":
                    surf_text = "Why so serious? - The Joker"
                else:
                    surf_text = f"{rank} of {suit} was already seen."
        else:
            surf_text = f"{player.name} is getting a card" + "." * (i // 3)

        surf = font.render(surf_text, False, BLACK)

        screen.blit(surf, surf.get_rect(midbottom=(600, 50)))
        pygame.display.update()
        i += 1
