import pygame
from Button import Button, turn_white, button_pressed
from Deck import BACK
from time import sleep


class Player:
    def __init__(self, name, balance, player_number, cards=None, wants_card=False, bet=1000, wants_bet=True):
        self.font = pygame.font.SysFont('comicsans', 20)
        self.font_small = pygame.font.SysFont('comicsans', 13)
        self.font_big = pygame.font.SysFont('comicsans', 30)
        if cards is None:
            cards = []
        self.name = name
        self.balance = balance
        self.cards = cards
        self.number = player_number
        self.surf = self.font.render(self.name, False, (10, 10, 10))
        self.surf_balance = self.font_small.render(f'Balance:{self.balance}', False, (10, 10, 10))
        self.wants_card = wants_card
        self.bet = bet
        self.wants_bet = wants_bet

    def show_name(self, window):
        window.blit(self.surf, self.surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 550)))
        window.blit(self.surf_balance, self.surf_balance.get_rect(topleft=(100 + 300 * (self.number - 1), 555)))

    def set_balance(self, new_balance):
        self.balance = new_balance

    def add_card(self, card):
        self.cards.append(card)

    def show_cards(self, window, result=False):
        if self.cards is None:
            self.cards = []

        if not self.name == 'Dealer':
            for i, card in enumerate(self.cards):
                window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1),
                            (100 + 300 * (self.number - 1) + 25 * i, 400))

        else:
            if len(self.cards) == 2:
                if not result:
                    if self.value_count_bj() == 21:
                        for i, card in enumerate(self.cards):
                            window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (560 + 25 * i, 50))

                    else:
                        window.blit(pygame.transform.rotozoom(self.cards[0].load_image(), 0, 1), (560, 50))
                        window.blit(pygame.transform.scale(BACK.load_image(), (500 * 0.15, 726 * 0.15)), (585, 50))
                else:
                    for i, card in enumerate(self.cards):
                        window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (560 + 25 * i, 50))

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
        if som > 21:
            for value in value_list:
                if value == 11:
                    ace_index = value_list.index(11)
                    value_list[ace_index] = 1
                    som = sum(value_list)
                    if som < 22:
                        return som
            self.wants_card = False
            return 0

    def value_count_hl(self):
        return len(self.cards)

    def display_score_bj(self, window, result=False):
        if len(self.cards) == 0:
            return False
        if not self.name == 'Dealer':
            if self.value_count_bj() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
            else:
                score_surf = self.font.render(str(self.value_count_bj()), False, (10, 10, 10))
            pygame.draw.rect(window, (31, 171, 57), (100 + 300 * (self.number - 1), 350, 50, 30))
            window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))

        else:
            if len(self.cards) == 2:
                if not result:
                    if self.cards[0].bj_value == 0:
                        score_surf = self.font.render(str(11), False, (10, 10, 10))
                    else:
                        score_surf = self.font.render(str(self.cards[0].bj_value), False, (10, 10, 10))
                    window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
                else:
                    if self.value_count_bj() == 21:
                        score_surf = self.font.render("Blackjack", False, (10, 10, 10))
                    else:
                        score_surf = self.font.render(str(self.value_count_bj()), False, (10, 10, 10))
                    pygame.draw.rect(window, (31, 171, 57), (550, 10, 100, 35))
                    window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
            elif self.value_count_bj() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
            else:
                score_surf = self.font.render(str(self.value_count_bj()), False, (10, 10, 10))
            pygame.draw.rect(window, (31, 171, 57), (550, 10, 100, 35))
            window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))

    def display_score_hl(self, window):
        if not self.name == 'Dealer':
            if self.value_count_hl() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
            else:
                score_surf = self.font.render(str(self.value_count_hl()), False, (10, 10, 10))
            window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
        else:
            if self.value_count_hl() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
            else:
                score_surf = self.font.render(str(self.value_count_hl()), False, (10, 10, 10))
            window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))

    def results(self, dealer_score, game):
        if game == 'bj':
            self_value = self.value_count_bj()
        else:
            self_value = self.value_count_hl()
        if self_value == 0:
            return 'bust: dealer wins', -1
        if dealer_score == self_value:
            return f'{self_value}: draw', 0
        if dealer_score > self_value:
            return f'{self_value}: dealer wins', -1
        if dealer_score < self_value:
            return f'{self_value}: you win', 1

    def display_results(self, window, dealer_score, game, dealer_blackjack=False):
        if dealer_blackjack:
            score_surf = self.font.render("dealer Blackjack", False, (10, 10, 10))
            window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
        else:
            score_surf = self.font.render(self.results(dealer_score, game)[0], False, (10, 10, 10))
            window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))

    def adjust_balance(self, dealer_score, game):
        self.balance += self.bet * self.results(dealer_score, game)[1]
        self.surf_balance = self.font_small.render(f'Balance:{self.balance}', False, (10, 10, 10))

    def place_bet(self, window, exit_button):
        self.bet = 0
        question_surf = self.font_big.render(f'{self.name}, how much do you want to bet?', False, (10, 10, 10))
        window.blit(question_surf, question_surf.get_rect(midbottom=(600, 250)))

        bet_buttons = [(i * 1000, Button((0, 0, 0), (325 + i * 75, 350), (50, 30), f'{i}k')) for i in range(1, 6)]

        bal = self.balance

        for bet_amount, button in bet_buttons:
            if bal >= bet_amount:
                button.draw(window)

        for event in pygame.event.get():
            if button_pressed(exit_button, event):
                return 'exit'

            for bet_amount, button in bet_buttons:
                if button_pressed(button, event) and bal >= bet_amount:
                    self.bet = bet_amount
