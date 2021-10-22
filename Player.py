import pygame


class Player:
    def __init__(self, name, balance, player_number, cards=None, wants_card=False):
        self.font = pygame.font.SysFont('comicsans', 20)
        self.font_small = pygame.font.SysFont('comicsans', 13)
        if cards is None:
            cards = []
        self.name = name
        self.balance = balance
        self.cards = cards
        self.number = player_number
        self.surf = self.font.render(self.name, False, (10, 10, 10))
        self.surf_balance = self.font_small.render('Balance:' + str(self.balance), False, (10, 10, 10))
        self.wants_card = wants_card

    def show_name(self, window):
        window.blit(self.surf, self.surf.get_rect(bottomleft=(100 + 300*(self.number - 1), 550)))
        window.blit(self.surf_balance, self.surf_balance.get_rect(topleft=(100 + 300*(self.number - 1), 555)))

    def set_balance(self, new_balance):
        self.balance = new_balance

    def add_card(self, card):
        self.cards.append(card)

    def show_cards(self, window):
        i = 0
        if not self.name == 'Dealer':
            for card in self.cards:
                window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1),
                            (100 + 300*(self.number - 1) + 25*i, 400))
                i += 1
        else:
            for card in self.cards:
                window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (560 + 25*i, 50))
                i += 1

    def value_count(self):
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

    def display_score(self, window):
        if not self.name == 'Dealer':
            if self.value_count() == 0:
                score_surf = self.font.render('bust', False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300 * (self.number - 1), 385)))
            else:
                score_surf = self.font.render(str(self.value_count()), False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(bottomleft=(100 + 300*(self.number - 1), 385)))
        else:
            if self.value_count() == 0:
                score_surf = self.font.render('Bust', False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))
            else:
                score_surf = self.font.render(str(self.value_count()), False, (10, 10, 10))
                window.blit(score_surf, score_surf.get_rect(midbottom=(600, 45)))

    def results(self, dealer_score):
        self_value = self.value_count()
        if str(self_value) == 'bust':
            return 'bust'
        if dealer_score == self_value:
            return 'draw'
        if dealer_score > self_value:
            return 'dealer wins'
        if dealer_score < self_value:
            return 'you win'