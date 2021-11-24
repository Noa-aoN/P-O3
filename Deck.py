import pygame
from random import shuffle

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


def load_random_deck():
    deck = [(rank, suit) for rank in range(len(RANKS[:-1])) for suit in range(len(SUITS))]
    shuffle(deck)
    return deck


def get_random_card(deck):
    if not deck:
        deck = load_random_deck()
        print("A new deck was created")

    rank, suit = deck.pop()

    return Card(0, 0, 0, 0, 0, rank, suit), deck


BACK = SpecialCard('Images/Cards/Card_Back.png', 0, 0)
