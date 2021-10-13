import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200, 600))
Clock = pygame.time.Clock()

test_font = pygame.font.Font('Font/Roboto-Regular.ttf', 20)
test_font_small = pygame.font.Font('Font/Roboto-Regular.ttf', 13)


class Card:
    def __init__(self, file, value):
        self.file = file
        self.value = value

    def load_image(self):
        return pygame.transform.rotozoom(pygame.image.load(self.file), 0, 0.15)


H1 = Card('PNG-cards-1.3/ace_of_hearts.png', 0)
H2 = Card('PNG-cards-1.3/2_of_hearts.png', 2)
H3 = Card('PNG-cards-1.3/3_of_hearts.png', 3)
H4 = Card('PNG-cards-1.3/4_of_hearts.png', 4)
H5 = Card('PNG-cards-1.3/5_of_hearts.png', 5)
H6 = Card('PNG-cards-1.3/6_of_hearts.png', 6)
H7 = Card('PNG-cards-1.3/7_of_hearts.png', 7)
H8 = Card('PNG-cards-1.3/8_of_hearts.png', 8)
H9 = Card('PNG-cards-1.3/9_of_hearts.png', 9)
H10 = Card('PNG-cards-1.3/10_of_hearts.png', 10)
H11 = Card('PNG-cards-1.3/jack_of_hearts2.png', 10)
H12 = Card('PNG-cards-1.3/queen_of_hearts2.png', 10)
H13 = Card('PNG-cards-1.3/king_of_hearts2.png', 10)

R1 = Card('PNG-cards-1.3/ace_of_diamonds.png', 0)
R2 = Card('PNG-cards-1.3/2_of_diamonds.png', 2)
R3 = Card('PNG-cards-1.3/3_of_diamonds.png', 3)
R4 = Card('PNG-cards-1.3/4_of_diamonds.png', 4)
R5 = Card('PNG-cards-1.3/5_of_diamonds.png', 5)
R6 = Card('PNG-cards-1.3/6_of_diamonds.png', 6)
R7 = Card('PNG-cards-1.3/7_of_diamonds.png', 7)
R8 = Card('PNG-cards-1.3/8_of_diamonds.png', 8)
R9 = Card('PNG-cards-1.3/9_of_diamonds.png', 9)
R10 = Card('PNG-cards-1.3/10_of_diamonds.png', 10)
R11 = Card('PNG-cards-1.3/jack_of_diamonds2.png', 10)
R12 = Card('PNG-cards-1.3/queen_of_diamonds2.png', 10)
R13 = Card('PNG-cards-1.3/king_of_diamonds2.png', 10)

S1 = Card('PNG-cards-1.3/ace_of_spades2.png', 0)
S2 = Card('PNG-cards-1.3/2_of_spades.png', 2)
S3 = Card('PNG-cards-1.3/3_of_spades.png', 3)
S4 = Card('PNG-cards-1.3/4_of_spades.png', 4)
S5 = Card('PNG-cards-1.3/5_of_spades.png', 5)
S6 = Card('PNG-cards-1.3/6_of_spades.png', 6)
S7 = Card('PNG-cards-1.3/7_of_spades.png', 7)
S8 = Card('PNG-cards-1.3/8_of_spades.png', 8)
S9 = Card('PNG-cards-1.3/9_of_spades.png', 9)
S10 = Card('PNG-cards-1.3/10_of_spades.png', 10)
S11 = Card('PNG-cards-1.3/jack_of_spades2.png', 10)
S12 = Card('PNG-cards-1.3/queen_of_spades2.png', 10)
S13 = Card('PNG-cards-1.3/king_of_spades2.png', 10)

K1 = Card('PNG-cards-1.3/ace_of_clubs.png', 0)
K2 = Card('PNG-cards-1.3/2_of_clubs.png', 2)
K3 = Card('PNG-cards-1.3/3_of_clubs.png', 3)
K4 = Card('PNG-cards-1.3/4_of_clubs.png', 4)
K5 = Card('PNG-cards-1.3/5_of_clubs.png', 5)
K6 = Card('PNG-cards-1.3/6_of_clubs.png', 6)
K7 = Card('PNG-cards-1.3/7_of_clubs.png', 7)
K8 = Card('PNG-cards-1.3/8_of_clubs.png', 8)
K9 = Card('PNG-cards-1.3/9_of_clubs.png', 9)
K10 = Card('PNG-cards-1.3/10_of_clubs.png', 10)
K11 = Card('PNG-cards-1.3/jack_of_clubs2.png', 10)
K12 = Card('PNG-cards-1.3/queen_of_clubs2.png', 10)
K13 = Card('PNG-cards-1.3/king_of_clubs2.png', 10)

screen.fill((31, 171, 57))

deck = [K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11, K12, K13,
        S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13,
        R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13,
        H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13]


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def set_balance(self, new_balance):
        self.balance = new_balance


player1 = Player('Matthias', 10000)
player2 = Player('Karel', 10000)
player3 = Player('Yannick', 10000)
player4 = Player('Jasper', 10000)

player1_surf = test_font.render(player1.name, False, (10, 10, 10))
player1_bal = test_font_small.render('Balance:' + str(player1.balance), False, (10, 10, 10))

player2_surf = test_font.render(player2.name, False, (10, 10, 10))
player2_bal = test_font_small.render('Balance:' + str(player2.balance), False, (10, 10, 10))

player3_surf = test_font.render(player3.name, False, (10, 10, 10))
player3_bal = test_font_small.render('Balance:' + str(player3.balance), False, (10, 10, 10))

player4_surf = test_font.render(player4.name, False, (10, 10, 10))
player4_bal = test_font_small.render('Balance:' + str(player4.balance), False, (10, 10, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(player1_surf, player1_surf.get_rect(bottomleft=(100, 550)))
    screen.blit(player1_bal, player1_bal.get_rect(topleft=(100, 555)))

    screen.blit(player2_surf, player2_surf.get_rect(bottomleft=(400, 550)))
    screen.blit(player2_bal, player2_bal.get_rect(topleft=(400, 555)))

    screen.blit(player3_surf, player3_surf.get_rect(bottomleft=(700, 550)))
    screen.blit(player3_bal, player3_bal.get_rect(topleft=(700, 555)))

    screen.blit(player4_surf, player4_surf.get_rect(bottomleft=(1000, 550)))
    screen.blit(player4_bal, player4_bal.get_rect(topleft=(1000, 555)))

    screen.blit(H1.load_image(), (0,0))

    pygame.display.update()
    Clock.tick(60)
