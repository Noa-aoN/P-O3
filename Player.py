import pygame
from Deck import BACK
from facenet_pytorch import MTCNN, InceptionResnetV1
from facenet_facerecognition import PlayerRegistration
from localdirectory import local_directory
from facenet_facerecognition import create_folder
import os
from Style import BLACK, WHITE, font, font_small, font_big




def Library():
    if os.path.exists(r"C:\Users"):
        projectdirectory = local_directory(r"C:\Users")
    elif os.path.exists(r"C:\Gebruikers"):
        projectdirectory = local_directory(r"C:\Gebruikers")
    else:
        projectdirectory = None
    librarydirectory = create_folder(os.path.join(projectdirectory, 'facenetLibraries'))
    library = PlayerRegistration(librarydirectory, 7)
    return library


def add_player(window, players, skip_button, active, player_name):
    name_box = pygame.Rect(490, 250, 220, 40)

    for event in pygame.event.get():
        if skip_button.button_pressed(event):
            return 'skip', None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if name_box.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    players.append(Player(player_name, 10000, len(players)))
                    full_name = player_name
                    return False, full_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

    if player_name:
        surf_text = player_name
    else:
        surf_text = f'Enter name of player {len(players) + 1}'

    if active:
        if player_name:
            surf_color = BLACK
        else:
            surf_color = WHITE
    else:
        surf_color = BLACK

    name_surf = font.render(surf_text, False, surf_color)
    window.blit(name_surf, name_surf.get_rect(topleft=(490, 250)))
    return active, player_name


class Player:
    def __init__(self, name, balance, player_number):
        self.name = name
        self.balance = balance
        self.bet = 0
        self.cards = []
        self.number = player_number
        self.wants_card = True
        self.wants_bet = True

    def __repr__(self):
        return self.name

    def __bool__(self):
        return self.balance >= 1000

    def show_name(self, window):
        pygame.draw.rect(window, (114, 200, 114), (40 + 290 * self.number, 370, 250, 220), 0, 3)
        name_surf = font.render(self.name, False, (10, 10, 10))
        window.blit(name_surf, name_surf.get_rect(topleft=(45 + 290 * self.number, 520)))

        balance_surf = font_small.render(f'Balance:{self.balance}', False, (10, 10, 10))
        window.blit(balance_surf, balance_surf.get_rect(topleft=(45 + 290 * self.number, 550)))

        bet_surf = font_small.render(f'Current bet:{self.bet}', False, (10, 10, 10))
        window.blit(bet_surf, bet_surf.get_rect(topleft=(45 + 290 * self.number, 565)))

    def add_card(self, card):
        self.cards.append(card)

    def show_cards(self, window, result=False):
        if not self.name == 'Dealer':
            for i, card in enumerate(self.cards):
                window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1),
                            (45 + 290 * self.number + 25 * i, 380))

        else:
            if len(self.cards) == 2 and not result:
                if self.value_count_bj() == 21:
                    for i, card in enumerate(self.cards):
                        window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (560 + 25 * i, 50))

                else:
                    window.blit(pygame.transform.rotozoom(self.cards[0].load_image(), 0, 1), (560, 50))
                    window.blit(pygame.transform.scale(BACK.load_image(), (500 * 0.15, 726 * 0.15)), (585, 50))

            else:
                for i, card in enumerate(self.cards):
                    window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (560 + 25 * i, 50))

    def value_count_bj(self):
        value_list = []
        for card in self.cards:
            if card.bj_value == 0:
                value_list.append(11)
            else:
                value_list.append(card.bj_value)
        som = sum(value_list)
        if som < 22:
            return som

        for value in value_list:
            if value == 11:
                ace_index = value_list.index(11)
                value_list[ace_index] = 1
                som = sum(value_list)
                if som < 22:
                    return som
        return 0

    def display_score_bj(self, window, result=False):
        if len(self.cards) == 0:
            return False
        if not self.name == 'Dealer':
            if self.value_count_bj() == 0:
                score_surf = font.render('Bust', False, (10, 10, 10))
            else:
                score_surf = font.render(str(self.value_count_bj()), False, (10, 10, 10))
            pygame.draw.rect(window, (31, 171, 57), (45 + 290 * self.number, 330, 50, 30))
            window.blit(score_surf, score_surf.get_rect(bottomleft=(45 + 290 * self.number, 365)))

        else:
            if len(self.cards) == 2:
                if not result:
                    if self.cards[0].bj_value == 0:
                        score_surf = font.render(str(11), False, (10, 10, 10))
                    else:
                        score_surf = font.render(str(self.cards[0].bj_value), False, (10, 10, 10))
                    window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
                else:
                    if self.value_count_bj() == 21:
                        score_surf = font.render("Blackjack", False, (10, 10, 10))
                    else:
                        score_surf = font.render(str(self.value_count_bj()), False, (10, 10, 10))
                    pygame.draw.rect(window, (31, 171, 57), (550, 10, 100, 35))
                    window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
            elif self.value_count_bj() == 0:
                score_surf = font.render('Bust', False, (10, 10, 10))
            else:
                score_surf = font.render(str(self.value_count_bj()), False, (10, 10, 10))
            pygame.draw.rect(window, (31, 171, 57), (550, 10, 100, 35))
            window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))

    def display_score_hl(self, window):
        score_surf = font.render(f"Total cards: {len(self.cards)}", False, (10, 10, 10))
        window.blit(score_surf, score_surf.get_rect(bottomleft=(45 + 290 * self.number, 365)))

    # Wordt niet gebruikt voor Higherlower
    def results(self, dealer_score, game, dealer_blackjack=False):
        self_value = self.value_count_bj()

        if self_value == 0:
            return 'bust: dealer wins', -1
        elif dealer_score == self_value:
            return f'{self_value}: draw', 0
        elif dealer_score > self_value or dealer_blackjack:
            return f'{self_value}: dealer wins', -1
        elif self_value == 21 and len(self.cards) == 2:
            return f'Blackjack: you win', 1.5
        elif dealer_score < self_value:
            return f'{self_value}: you win', 1

    def display_results(self, window, dealer_score, game, dealer_blackjack=False):
        if dealer_blackjack:
            score_surf = font.render("Dealer Blackjack", False, (10, 10, 10))
        else:
            score_surf = font.render(self.results(dealer_score, game)[0], False, (10, 10, 10))

        window.blit(score_surf, score_surf.get_rect(bottomleft=(45 + 290 * self.number, 365)))

    def adjust_balance(self, dealer_score, game, blackjack=False):
        self.balance += int(self.bet * self.results(dealer_score, game, blackjack)[1])

    def draw_bet_buttons(self, window, bet_buttons):
        question_surf = font_big.render(f'{self.name}, how much do you want to bet?', False, (10, 10, 10))
        window.blit(question_surf, question_surf.get_rect(midbottom=(600, 250)))

        for bet_amount, button in bet_buttons:
            if self.balance >= bet_amount:
                button.draw(window)
