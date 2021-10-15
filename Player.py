import pygame


class Player:
    def __init__(self, name, balance, player_number, cards=None):
        font = pygame.font.SysFont('comicsans', 20)
        font_small = pygame.font.SysFont('comicsans', 13)

        if cards is None:
            cards = []
        self.name = name
        self.balance = balance
        self.cards = cards
        self.number = player_number
        self.surf = font.render(self.name, False, (10, 10, 10))
        self.surf_balance = font_small.render('Balance:' + str(self.balance), False, (10, 10, 10))

    def show_name(self, window):
        window.blit(self.surf, self.surf.get_rect(bottomleft=(100 + 300*(self.number - 1), 550)))
        window.blit(self.surf_balance, self.surf_balance.get_rect(topleft=(100 + 300*(self.number - 1), 555)))

    def set_balance(self, new_balance):
        self.balance = new_balance

    def add_card(self, card):
        self.cards.append(card)

    def show_cards(self, window):
        i = 0
        for card in self.cards:
            window.blit(pygame.transform.rotozoom(card.load_image(), 0, 1), (100 + 300*(self.number - 1) + 25*i, 375))
            i += 1

    def value_count(self):
        value_list = []
        for card in self.cards:
            if card[1] == 0:
                value_list.append(11)
            else:
                value_list.append(card[1])
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
            return som
