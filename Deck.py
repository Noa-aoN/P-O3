import pygame


class Card:
    def __init__(self, file, bj_value, hl_value):
        self.file = file
        self.bj_value = bj_value
        self.hl_value = hl_value

    def load_image(self):
        return pygame.transform.rotozoom(pygame.image.load(self.file), 0, 0.15)


SUITS = ("hearts", "diamonds", "spades", "clubs")
RANKS = ("ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king")
BJ_VALUES = (0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)
HL_VALUES = (14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

deck = []

for suit in SUITS:
    for i, rank in enumerate(RANKS):
        deck.append(Card(f"PNG-cards-1.3/{rank}_of_{suit}.png", BJ_VALUES[i], HL_VALUES[i]))

BACK = Card('PNG-cards-1.3/Back.png', 0, 0)
