import pygame


class musicManager():

    def __init__(self):
        # Setting up music
        pygame.mixer.music.load("music/1-Lex.wav")  
        pygame.mixer.music.set_volume(0.5)

    def play(self):

        pygame.mixer.music.play(-1)
