import pygame
from random import choice

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
         "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Joker")
BJ_VALUES = (0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 0)
HL_VALUES = (14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0)


class Card:
    def __init__(self, contour, pts, w, h, center, rank, suit):
        self.contour = contour  # Contour of card
        self.corner_pts = pts  # Corner points of card
        self.dim = (w, h)  # Width and height of card
        self.center = center  # Center point of card
        self.rank = rank  # Index of the rank
        self.suit = suit  # Index of the suit
        self.bj_value = BJ_VALUES[rank]
        self.hl_value = HL_VALUES[rank]

    def get_rank_suit(self):
        suit = SUITS[self.suit]
        rank = RANKS[self.rank]
        return rank, suit

    def load_image(self):
        rank, suit = self.get_rank_suit()
        file = f"Images/Cards/{rank}_{suit}.png"
        return pygame.transform.rotozoom(pygame.image.load(file), 0, 0.15)


class SpecialCard:
    def __init__(self, file, bj_value, hl_value):
        self.file = file
        self.bj_value = bj_value
        self.hl_value = hl_value

    def load_image(self):
        return pygame.transform.rotozoom(pygame.image.load(self.file), 0, 0.15)


def load_deck():
    return [[(rank, suit) for rank in range(len(RANKS[:-1]))] for suit in range(len(SUITS))]


def get_random_card(deck):
    suit_list = choice(deck)
    i, j = choice(suit_list)
    print(i, j)

    del deck[j][i]

    card = Card(0, 0, 0, 0, 0, i, j)

    return card, deck


BACK = SpecialCard('Images/Cards/Card_Back.png', 0, 0)
