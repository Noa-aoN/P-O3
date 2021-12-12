import pygame
from Deck import load_random_deck, get_random_card
from Detection.gestures_mediapipe import LandmarkGetter
from Player import Dealer, Library
from Camera import get_camera_card
from Style import font_huge, GREEN, BLACK, WHITE, BLUE
from Button import common_buttons, hl_buttons, bj_buttons


# from carddispencer_functies import setup, dcmotor_rotate, servo_rotate , servo_rotate_fromto


def home_screen_hl(game, screen, buttons):
    title_surf = font_huge.render('Higher Lower', False, WHITE)
    screen.blit(title_surf, title_surf.get_rect(midbottom=(597, 157)))
    title_surf2 = font_huge.render('Higher Lower', False, BLACK)
    screen.blit(title_surf2, title_surf2.get_rect(midbottom=(600, 160)))
    H = pygame.transform.rotozoom(pygame.image.load("Images/Arrows.jpg"), 0, 0.5)
    screen.blit(pygame.transform.rotozoom(H, 0, 2), (530, 210))
    for name, option in [("cam", game.cam), ("rasp", game.rasp), ("link", game.with_linking)]:
        if option:
            game.buttons[name].set_color(BLUE)
        else:
            game.buttons[name].set_color(BLACK)

    buttons["start"].draw(screen)
    buttons["cam"].draw(screen)
    buttons["rasp"].draw(screen)
    buttons["link"].draw(screen)
    buttons["rules"].draw(screen)
    buttons["exit"].draw(screen)


def home_screen_bj(game, screen, buttons):
    Blackjack_surf2 = font_huge.render('Blackjack', False, WHITE)
    screen.blit(Blackjack_surf2, Blackjack_surf2.get_rect(midbottom=(597, 157)))
    Blackjack_surf = font_huge.render('Blackjack', False, BLACK)
    screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600, 160)))
    H = pygame.transform.rotozoom(pygame.image.load("Images/Cards/Jack_Spades.png"), 0, 0.15)
    S = pygame.transform.rotozoom(pygame.image.load("Images/Cards/Ace_Hearts.png"), 0, 0.15)
    screen.blit(pygame.transform.rotozoom(H, 10, 1.2), (510, 230))
    screen.blit(pygame.transform.rotozoom(S, -10, 1.2), (590, 230))

    for name, option in [("cam", game.cam), ("rasp", game.rasp), ("link", game.with_linking)]:
        if option:
            game.buttons[name].set_color(BLUE)
        else:
            game.buttons[name].set_color(BLACK)

    buttons["start"].draw(screen)
    buttons["cam"].draw(screen)
    buttons["rasp"].draw(screen)
    buttons["link"].draw(screen)
    buttons["rules"].draw(screen)
    buttons["exit"].draw(screen)


def restart_game_screen(game, screen, buttons):
    pygame.draw.rect(screen, GREEN, (0, 340, 1200, 25), 0)
    game_over_surf = font_huge.render('Game Over', False, (255, 0, 0))
    screen.blit(game_over_surf, game_over_surf.get_rect(midbottom=(600, 150)))
    buttons["exit"].draw(screen)
    buttons["restart"].draw(screen)


class Game:
    def __init__(self, screen, players, draw_screen, buttons):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.players = list(players)
        self.players_reset()
        self.player_memory = list(players)
        self.player_index = 0
        self.draw_screen = draw_screen
        self.cap_gest = None
        self.cap_card = None
        self.buttons = buttons
        self.library = Library()
        self.landmarkgetter = LandmarkGetter()
        self.gest_time = 0
        self.cameracooldown = True
        self.deck = load_random_deck()
        self.first_card = True
        self.with_linking = False
        self.cam = False
        self.rasp = False

    def __call__(self):
        self.screen.fill(GREEN)
        self.draw_screen(self, self.screen, self.buttons)
        pygame.display.update()
        self.clock.tick(20)
        
    def players_reset(self):
        for player in self.players:
            player.reset()

    def get_card_func(self, player):
        if self.cam:
            return get_camera_card(self, player)
        return get_random_card(self, player)

    def give_card(self):
        #print("geef nieuwe kaart")
        if self.rasp:
            dcmotor_rotate()

    def rotate_fromto_player(self, previous_player, player):
        #print("ga van", previous_player, "naar", player)
        if self.rasp:
            servo_rotate_fromto(previous_player, player)

    def rotate_to(self, player):
        #print("ga naar", player)
        if self.rasp:
            servo_rotate(player)

    def get_current_player(self):
        return self.players[self.player_index]

    def next_player(self):
        if self.player_index == len(self.players) - 1:
            self.player_index = 0
        else:
            self.player_index += 1
        #print("current player ok" + str(self.player_index))


class Blackjack(Game):
    def __init__(self, screen, players):
        super().__init__(screen, players, home_screen_bj, dict(common_buttons, **bj_buttons))
        self.dealer = Dealer()
        self.previous_player = 0
        self.last_fingers = None
        self.last_option = None

    def play_again(self):
        self.filter_players()
        self.deck = load_random_deck()
        self.player_index = 0
        self.previous_player = 0
        self.gest_time = 0
        self.last_fingers = None
        self.last_option = None
        self.cameracooldown = True
        self.first_card = True
        self.dealer.cards = []

        for player in self.players:
            player.cards = []
            player.bet = 0
            player.wants_bet = True
            player.wants_card = True
            player.wants_card = True

    def show_each_player(self):
        for player in self.players:
            player.show_name(self.screen)
            player.show_cards(self.screen)
            player.display_score_bj(self.screen)

    def filter_players(self):
        self.players = list(filter(lambda player: 1000 <= player.balance, self.players))
        if len(self.players) == 0:
            self.draw_screen = restart_game_screen

    def next_player(self):
        if self.player_index + 1 < len(self.players):
            self.player_index += 1
        else:
            self.player_index = 0
        print("current player ok"+ str(self.player_index))
        self.players = list(filter(lambda player: player, self.players))
        if not self.players:
            self.players = list(self.player_memory)
            self.draw_screen = restart_game_screen

    def everyone_bust(self):
        return all([player.value_count_bj() == 0 for player in self.players])


class Higherlower(Game):
    def __init__(self, screen, players):
        super().__init__(screen, players, home_screen_hl, dict(common_buttons, **hl_buttons))
        self.last_index = None
        self.last_fingers = None

    def show_each_player(self):
        for player in self.players:
            player.show_name(self.screen)
            player.show_cards(self.screen)
            player.display_score_bj(self.screen)
            
    def subtract_bets(self):
        for player in self.players:
            player.balance -= player.bet

    def play_again(self, cur_player=None):
        self.deck = load_random_deck()
        self.gest_time = 0
        self.cameracooldown = True
        self.first_card = True
        if cur_player is not None:
            if cur_player.balance < 1000:
                cur_player.wants_bet = False
            else:
                cur_player.wants_bet = True
            cur_player.cards = []
            cur_player.bet = 0
            cur_player.prize_money = 0
        else:
            for player in self.players:
                if not player.balance < 1000:
                    player.wants_bet = True
                else:
                    player.wants_bet = False
                player.cards = []
                player.bet = 0
                player.prize_money = 0
