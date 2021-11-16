import pygame
from Button import Button, turn_white, button_pressed


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
        self.surf_balance = self.font_small.render('Balance:' + str(self.balance), False, (10, 10, 10))
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

    def show_cards(self, window):
        if self.cards is None:
            self.cards = []
        i = 0
        if not self.name == 'Dealer':
            for card in self.cards:
                window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1),
                            (100 + 300 * (self.number - 1) + 25 * i, 400))
                i += 1
        else:
            for card in self.cards:
                window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (560 + 25 * i, 50))
                i += 1

    def value_count_bj(self):
        value_list = []
        for card in self.cards:
            if card.value == 0:
                value_list.append(11)
            else:
                value_list.append(card.value)
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

    def display_score_bj(self, window):
        if not self.name == 'Dealer':
            if self.value_count_bj() == 0:
                score_surf = self.font.render('bust', False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
            else:
                score_surf = self.font.render(str(self.value_count_bj()), False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
        else:
            if self.value_count_bj() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
            else:
                score_surf = self.font.render(str(self.value_count_bj()), False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))

    def display_score_hl(self, window):
        if not self.name == 'Dealer':
            if self.value_count_hl() == 0:
                score_surf = self.font.render('bust', False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
            else:
                score_surf = self.font.render(str(self.value_count_hl()), False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
        else:
            if self.value_count_hl() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
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
            return str(self_value) + ': draw', 0
        if dealer_score > self_value:
            return str(self_value) + ': dealer wins', -1
        if dealer_score < self_value:
            return str(self_value) + ': you win', 1

    def display_results(self, window, dealer_score, game):
        score_surf = self.font.render(self.results(dealer_score, game)[0], False, (10, 10, 10))
        window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))

    def adjust_balance(self, dealer_score, game):
        self.balance += self.bet * self.results(dealer_score, game)[1]
        self.surf_balance = self.font_small.render('Balance:' + str(self.balance), False, (10, 10, 10))

    def place_bet(self, window):
        self.bet = 0
        question_surf = self.font_big.render(str(self.name) + ', how much do you want to bet?', False, (10, 10, 10))
        window.blit(question_surf, question_surf.get_rect(midbottom=(600, 250)))
        button_1 = Button((0, 0, 0), (400, 350), (50, 30), '1k')
        button_2 = Button((0, 0, 0), (475, 350), (50, 30), '2k')
        button_3 = Button((0, 0, 0), (550, 350), (50, 30), '3k')
        button_4 = Button((0, 0, 0), (625, 350), (50, 30), '4k')
        button_5 = Button((0, 0, 0), (700, 350), (50, 30), '5k')
        if self.balance >= 1000:
            button_1.draw(window)
        if self.balance >= 2000:
            button_2.draw(window)
        if self.balance >= 3000:
            button_3.draw(window)
        if self.balance >= 4000:
            button_4.draw(window)
        if self.balance >= 5000:
            button_5.draw(window)

        for event in pygame.event.get():
            if button_pressed(button_1, event) and self.balance >= 1000:
                self.bet = 1000
            elif button_pressed(button_2, event) and self.balance >= 2000:
                self.bet = 2000
            elif button_pressed(button_3, event) and self.balance >= 3000:
                self.bet = 3000
            elif button_pressed(button_4, event) and self.balance >= 4000:
                self.bet = 4000
            elif button_pressed(button_5, event) and self.balance >= 5000:
                self.bet = 5000
