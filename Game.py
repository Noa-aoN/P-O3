import pygame
import socket
from time import sleep
from Deck import load_random_deck, get_random_card
from Detection.gestures_mediapipe import LandmarkGetter
from Player import Dealer, Library
from Camera import get_camera_card
from Style import font_huge, GREEN, BLACK, WHITE, BLUE


def home_screen_hl(game, screen, buttons, x_scale, y_scale):
    title_surf = font_huge.render('Higher Lower', False, WHITE)
    screen.blit(title_surf, title_surf.get_rect(midbottom=(597*x_scale, 157*y_scale)))
    title_surf2 = font_huge.render('Higher Lower', False, BLACK)
    screen.blit(title_surf2, title_surf2.get_rect(midbottom=(600*x_scale, 160*y_scale)))
    H = pygame.transform.rotozoom(pygame.image.load("Images/Arrows.jpg"), 0, 0.5)
    screen.blit(pygame.transform.rotozoom(H, 0, 2), (530*x_scale, 210*y_scale))
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


def home_screen_bj(game, screen, buttons, x_scale, y_scale):
    Blackjack_surf2 = font_huge.render('Blackjack', False, WHITE)
    screen.blit(Blackjack_surf2, Blackjack_surf2.get_rect(midbottom=(597*x_scale, 157*y_scale)))
    Blackjack_surf = font_huge.render('Blackjack', False, BLACK)
    screen.blit(Blackjack_surf, Blackjack_surf.get_rect(midbottom=(600*x_scale, 160*y_scale)))
    H = pygame.transform.rotozoom(pygame.image.load("Images/Cards/Jack_Spades.png"), 0, 0.15)
    S = pygame.transform.rotozoom(pygame.image.load("Images/Cards/Ace_Hearts.png"), 0, 0.15)
    screen.blit(pygame.transform.rotozoom(H, 10, 1.2), (510*x_scale, 230*y_scale))
    screen.blit(pygame.transform.rotozoom(S, -10, 1.2), (590*x_scale, 230*y_scale))

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


def restart_game_screen(game, screen, buttons, x_scale, y_scale):
    pygame.draw.rect(screen, GREEN, (0, 340*y_scale, 1200*x_scale, 25*y_scale), 0)
    game_over_surf = font_huge.render('Game Over', False, (255, 0, 0))
    screen.blit(game_over_surf, game_over_surf.get_rect(midbottom=(600*x_scale, 150*y_scale)))
    buttons["exit"].draw(screen)
    buttons["restart"].draw(screen)


class Game:
    def __init__(self, screen, players, draw_screen, buttons, x_scale, y_scale):
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
        self.with_linking = False
        self.cam = False
        self.rasp = False
        self.client = None
        self.previous_player = 0
        self.x_scale = x_scale
        self.y_scale = y_scale

    def __call__(self):
        self.screen.fill(GREEN)
        self.draw_screen(self, self.screen, self.buttons, self.x_scale, self.y_scale)
        pygame.display.update()
        self.clock.tick(20)

    def create_client(self):
        if self.rasp:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(("172.20.10.13", 5050))
            self.send("CONNECTED !")
            num = self.players[0].number
            self.rotate_to(num)
            self.previous_player = num

    def send(self, msg):
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (64 - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode('utf-8'))

    def players_reset(self):
        for player in self.players:
            player.reset()

    def get_card_func(self, player):
        if self.rasp:
            sleep(1)
            self.send("GIVE CARD")

        if self.cam:
            return get_camera_card(self, player)

        return get_random_card(self, player)

    def rotate_fromto_player(self, previous_player, player):
        self.previous_player = player
        if self.rasp:
            sleep(1)
            self.send(f"ROTATE {previous_player} {player}")

    def rotate_to(self, player):
        if self.rasp:
            sleep(1)
            self.send(f"ROTATE {player}")

    def get_current_player(self):
        return self.players[self.player_index]


class Blackjack(Game):
    def __init__(self, screen, players, buttons, x_scale, y_scale):
        super().__init__(screen, players, home_screen_bj, buttons, x_scale, y_scale)
        self.dealer = Dealer(x_scale, y_scale)
        self.last_fingers = None
        self.last_option = None

    def play_again(self):
        self.filter_players()
        self.deck = load_random_deck()
        self.gest_time = 0
        self.last_fingers = None
        self.last_option = None
        self.cameracooldown = True
        self.dealer.cards = []
        if not self.players:
            self.player_index = 0
        else:
            self.player_index = self.players[0].number
        self.rotate_fromto_player(self.previous_player, self.player_index)

        for player in self.players:
            player.reset()

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
        self.players = list(filter(lambda player: player, self.players))
        if not self.players:
            self.players = list(self.player_memory)
            self.draw_screen = restart_game_screen

    def everyone_bust(self):
        return all([player.value_count_bj() == 0 for player in self.players])


class Higherlower(Game):
    def __init__(self, screen, players, buttons, x_scale, y_scale):
        super().__init__(screen, players, home_screen_hl, buttons, x_scale, y_scale)
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

    def next_player(self):
        if self.player_index == len(self.players) - 1:
            self.player_index = 0
        else:
            self.player_index += 1
