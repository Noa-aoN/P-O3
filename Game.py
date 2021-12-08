import pygame
from Deck import load_random_deck, get_random_card
from gestures_mediapipe import LandmarkGetter
from Player import Player
from Camera import get_camera_card
from Style import font_big, GREEN


def legefunctie():
    print("geef nieuwe kaart")


def legefunctie_2(previous_player, player):
    print("ga van", previous_player, "naar", player)


def legefunctie_3(player):
    print("ga naar", player)


def restart_game_screen(game, screen, buttons):
    pygame.draw.rect(screen, GREEN, (0, 340, 1200, 25), 0)
    game_over_surf = font_big.render('Game Over', False, (255, 0, 0))
    screen.blit(game_over_surf, game_over_surf.get_rect(midbottom=(600, 150)))
    buttons["exit"].draw(screen)
    buttons["restart"].draw(screen)


class Game:
    def __init__(self, screen, draw_screen, players, buttons, library, camera, with_rasp):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.players = list(players)
        self.player_memory = list(players)
        self.player_index = 0
        self.draw_screen = draw_screen
        self.cap_gest = None
        self.cap_card = None
        self.buttons = buttons
        self.library = library
        self.landmarkgetter = LandmarkGetter()
        self.gest_time = 0
        self.cameracooldown = True
        self.deck = load_random_deck()
        self.first_card = True

        if camera:
            self.get_card_func = get_camera_card
        else:
            self.get_card_func = get_random_card

        if with_rasp:
            self.give_card = dcmotor_rotate
            self.rotate_fromto_player = servo_rotate_fromto
            self.rotate_to = servo_rotate
        else:
            self.give_card = legefunctie
            self.rotate_fromto_player = legefunctie_2
            self.rotate_to = legefunctie_3

    def __call__(self):
        self.screen.fill(GREEN)
        self.draw_screen(self, self.screen, self.buttons)
        pygame.display.update()
        self.clock.tick(60)

    def get_current_player(self):
        return self.players[self.player_index]

    def next_player(self):
        if self.player_index == len(self.players) - 1:
            self.player_index = 0
        else:
            self.player_index += 1
        print("current player " + str(self.player_index))


class Blackjack(Game):
    def __init__(self, screen, draw_screen, players, buttons, library, camera, with_rasp, with_linking):
        super().__init__(screen, draw_screen, players, buttons, library, camera, with_rasp)
        self.dealer = Player('Dealer', 0, 0)
        self.previous_player = 0
        self.last_fingers = None
        self.last_option = None
        self.with_linking = with_linking

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
            player.wants_card = False

    def show_each_player(self):
        for player in self.players:
            player.show_name(self.screen)
            player.show_cards(self.screen)
            player.display_score_bj(self.screen)

    def filter_players(self):
        self.players = list(filter(lambda player: 1000 <= player.balance, self.players))
        if not self.players:
            self.players = list(self.player_memory)
            self.draw_screen = restart_game_screen

    def everyone_bust(self):
        return all([player.value_count_bj() == 0 for player in self.players])


class Higherlower(Game):
    def __init__(self, screen, draw_screen, players, buttons, library, camera, with_rasp):
        super().__init__(screen, draw_screen, players, buttons, library, camera, with_rasp)
        self.last_index = None

    def play_again(self):
        self.deck = load_random_deck()
        self.gest_time = 0
        self.cameracooldown = True
        self.first_card = True
        for player in self.players:
            player.cards = []
            player.bet = 0
