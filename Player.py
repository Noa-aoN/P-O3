import os
import pygame
from Deck import BACK
from Detection.facenet_facerecognition import PlayerRegistration
# from localdirectory import local_directory
from Detection.facenet_facerecognition import create_folder
from Style import BLACK, WHITE, GREEN, font, font_small, font_big


def Library():
    librarydirectory = create_folder(os.path.join(os.path.expanduser('~'), 'facenetLibraries'))
    library = PlayerRegistration(librarydirectory, 7)
    return library


def add_player(window, players, skip_button, active, player_name, x_scale, y_scale):
    name_box = pygame.Rect(490*x_scale, 250*y_scale, 220*x_scale, 40*y_scale)

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
                    players.append(Player(player_name, 10000, len(players), x_scale, y_scale))
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
    window.blit(name_surf, name_surf.get_rect(topleft=(490*x_scale, 250*y_scale)))
    return active, player_name


class Player:
    def __init__(self, name, balance, player_number, x_scale, y_scale):
        self.name = name
        self.balance = balance
        self.bet = 0
        self.cards = []
        self.number = player_number
        self.wants_card = True
        self.wants_bet = True
        self.prev_prize = 0
        self.prize_money = 0
        self.prize_money_coefs = [25 / 3, 37.5, 475 / 6]  # a*x^3 + b*x^2 + c*x for a bet of 1k
        self.wants_restart = False
        self.x_scale = x_scale
        self.y_scale = y_scale

    def __repr__(self):
        return self.name

    def __bool__(self):
        return self.balance >= 1000

    def reset(self):
        self.bet = 0
        self.cards = []
        self.wants_card = True
        self.wants_bet = True
        self.prev_prize = 0
        self.prize_money = 0
        self.wants_restart = False

    def show_name(self, window, hl_game=False):
        i = self.number
        width_background = 250*self.x_scale
        if hl_game:
            i = 0
            width_background = 1120*self.x_scale

        pygame.draw.rect(window, (114, 200, 114), (40*self.x_scale + 290*self.x_scale * i, 370*self.y_scale, width_background, 220*self.y_scale), 0, 3)
        name_surf = font.render(self.name, False, (10, 10, 10))
        window.blit(name_surf, name_surf.get_rect(topleft=(45*self.x_scale + 290*self.x_scale * i, 520*self.y_scale)))

        balance_surf = font_small.render(f'Balance:{self.balance}', False, (10, 10, 10))
        window.blit(balance_surf, balance_surf.get_rect(topleft=(45*self.x_scale + 290*self.x_scale * i, 550*self.y_scale)))

        bet_surf = font_small.render(f'Current bet:{self.bet}', False, (10, 10, 10))
        window.blit(bet_surf, bet_surf.get_rect(topleft=(45*self.x_scale + 290*self.x_scale * i, 565*self.y_scale)))

    def show_prize_money(self, window, hl_game=False):
        i = self.number
        if hl_game:
            i = 0
        surf_prize_money = font_small.render(f'+ {self.prize_money}', False, (10, 10, 10))
        window.blit(surf_prize_money, surf_prize_money.get_rect(topleft=(160*self.x_scale + 290*self.x_scale * i, 550*self.y_scale)))

    def add_card(self, card):
        self.cards.append(card)

    def show_cards(self, window, hl_game=False):
        j = self.number
        if hl_game:
            j = 0
        for i, card in enumerate(self.cards):
            window.blit(card.load_image(), (45*self.x_scale + 290*self.x_scale * j + 25*self.x_scale * i, 380*self.y_scale))

    def value_count_bj(self):
        value_list = []
        for card in self.cards:
            if card.bj_value == -1:
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

    def display_score_bj(self, window):
        if len(self.cards) == 0:
            return False
        if self.value_count_bj() == 0:
            score_surf = font.render('Bust', False, (10, 10, 10))
        else:
            score_surf = font.render(str(self.value_count_bj()), False, (10, 10, 10))
        pygame.draw.rect(window, (31, 171, 57), (45*self.x_scale + 290*self.x_scale * self.number, 330*self.y_scale, 50*self.x_scale, 30*self.y_scale))
        window.blit(score_surf, score_surf.get_rect(bottomleft=(45*self.x_scale + 290*self.x_scale * self.number, 365*self.y_scale)))

    def display_score_hl(self, window, hl_game=False):
        i = self.number
        if hl_game:
            i = 0
        score_surf = font.render(f"Total cards: {len(self.cards)}", False, (10, 10, 10))
        window.blit(score_surf, score_surf.get_rect(bottomleft=(45*self.x_scale + 290*self.x_scale * i, 365*self.y_scale)))

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

        window.blit(score_surf, score_surf.get_rect(bottomleft=(45*self.x_scale + 290*self.x_scale * self.number, 365*self.y_scale)))

    def adjust_balance(self, dealer_score, game, blackjack=False):
        self.balance += int(self.bet * self.results(dealer_score, game, blackjack)[1])

    def draw_bet_buttons(self, window, bet_buttons):
        question_surf = font_big.render(f'{self.name}, how much do you want to bet?', False, (10, 10, 10))
        window.blit(question_surf, question_surf.get_rect(midbottom=(600*self.x_scale, 250*self.y_scale)))

        for bet_amount, button in bet_buttons:
            if self.balance >= bet_amount:
                button.draw(window)

    def calculate_prize_money(self):
        factor = self.bet / 1000
        coefs = list(map(lambda y: y * factor, self.prize_money_coefs))
        x = len(self.cards) - 1
        self.prize_money = int(coefs[0] * (x ** 3) - coefs[1] * (x ** 2) + coefs[2] * x) + self.prev_prize

    def reset_money(self):
        self.bet = 0
        self.prize_money = 0
        self.prev_prize = 0


class Dealer:
    def __init__(self, x_scale, y_scale):
        self.name = "Dealer"
        self.cards = []
        self.has_dummy = False
        self.x_scale = x_scale
        self.y_scale = y_scale

    def add_card(self, card):
        self.cards.append(card)

    def add_hidden_card(self):
        self.has_dummy = True
        self.cards.append(BACK)

    def show_cards(self, window):
        for i, card in enumerate(self.cards):
            window.blit(card.load_image(), (560*self.x_scale + 25*self.x_scale * i, 50*self.y_scale))

    def value_count_bj(self):
        value_list = []
        for card in self.cards:
            if card.bj_value == -1:
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

    def display_score_bj(self, window, blackjack=False):
        # Otherwise bust is displayed
        if len(self.cards) == 0:
            return False

        if blackjack:
            score_surf = font.render("Blackjack", False, (10, 10, 10))
        elif self.value_count_bj() == 0:
            score_surf = font.render('Bust', False, (10, 10, 10))
        else:
            score_surf = font.render(str(self.value_count_bj()), False, (10, 10, 10))

        pygame.draw.rect(window, GREEN, (550*self.x_scale, 10*self.y_scale, 100*self.x_scale, 35*self.y_scale))
        window.blit(score_surf, score_surf.get_rect(midbottom=(600*self.x_scale, 45*self.y_scale)))
