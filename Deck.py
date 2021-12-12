from cv2 import imread, IMREAD_GRAYSCALE
import pygame
from random import shuffle

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
         "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Joker")

SUITS_IMG = [imread(f"Images/MyMoulds/{suit}.jpg", IMREAD_GRAYSCALE) for suit in SUITS]
RANKS_IMG = [imread(f"Images/MyMoulds/{rank}.jpg", IMREAD_GRAYSCALE) for rank in RANKS]

TEMPLATE_SUITS_IMG = imread("Images/References/ReferenceSuits.jpg", IMREAD_GRAYSCALE)
TEMPLATE_RANKS_IMG = imread("Images/References/ReferenceRanks.jpg", IMREAD_GRAYSCALE)

BJ_VALUES = (-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 0)
HL_VALUES = (14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0)


class Card:
    def __init__(self, contour, pts, w, h, center, rank, suit, match=0):
        self.contour = contour  # Contour of card
        self.corner_pts = pts  # Corner points of card
        self.dim = (w, h)  # Width and height of card
        self.center = center  # Center point of card
        self.rank = rank  # Index of the rank
        self.suit = suit  # Index of the suit
        self.bj_value = BJ_VALUES[rank]
        self.hl_value = HL_VALUES[rank]
        self.match = match

    def __bool__(self):
        return self.rank != -1 and self.suit != -1

    def get_rank_suit(self):
        assert self.rank != -1 and self.suit != -1
        suit = SUITS[self.suit]
        rank = RANKS[self.rank]
        return rank, suit

    def load_image(self):
        rank, suit = self.get_rank_suit()
        if rank == "Joker":
            file = f"Images/Cards/Ace_Hearts.png"
        else:
            file = f"Images/Cards/{rank}_{suit}.png"
        return pygame.transform.rotozoom(pygame.image.load(file).convert_alpha(), 0, 0.15)


class SpecialCard:
    def __init__(self, file, bj_value, hl_value):
        self.file = file
        self.bj_value = bj_value
        self.hl_value = hl_value

    def load_image(self):
        img = pygame.transform.scale(pygame.image.load(self.file), (500, 726))
        return pygame.transform.rotozoom(img.convert_alpha(), 0, 0.15)


def load_random_deck():
    deck = [(rank, suit) for rank in RANKS[:-1] for suit in SUITS]
    shuffle(deck)
    return deck


def get_random_card(game, player):
    deck = game.deck
    if not deck:
        deck = load_random_deck()
        print("A new deck was created")

    cardname = deck.pop()
    rank, suit = cardname
    i = RANKS.index(rank)
    j = SUITS.index(suit)

    player.add_card(Card(0, 0, 0, 0, 0, i, j))
    game.deck = deck


BACK = SpecialCard('Images/Cards/Card_Back.png', 0, 0)
