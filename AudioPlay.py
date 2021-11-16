import pygame

pygame.mixer.init()
pygame.init()


def playsound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)
    pygame.event.wait()


playsound("DroppingChips.wav")