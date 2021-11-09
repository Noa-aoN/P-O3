import pygame
from Button import Button, turn_white
from BlackJack import blackjack
from HigherLower import higherlower


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()

    font_big = pygame.font.Font('Font/Roboto-Regular.ttf', 80)
    font = pygame.font.Font('Font/Roboto-Regular.ttf', 25)

    bj_button = Button((0, 0, 0), (300, 480), (180, 65), 'Blackjack')
    hl_button = Button((0, 0, 0), (550, 480), (260, 65), 'Higher Lower')

    choose_game = font_big.render('Choose Game', False, (0, 0, 0))

    while True:
        pygame.display.update()
        screen.fill((31, 171, 57))
        screen.blit(choose_game, choose_game.get_rect(midbottom=(600, 150)))
        bj_button.draw(screen)
        hl_button.draw(screen)

        buttons = [bj_button, hl_button]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.collides(pos):
                        turn_white(button, event)
                        game = button.text
                        if game == "Blackjack":
                            blackjack(screen, clock)
                        elif game == "Higher Lower":
                            higherlower(screen, clock)

        clock.tick(60)

if __name__ == '__main__':
    main_menu()
