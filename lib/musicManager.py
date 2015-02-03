import pygame


class musicManager():
    
    def __init__(self):
        # Setting up music
        pygame.mixer.music.load("music/1-Lex.wav")
        pygame.mixer.music.queue("music/2-Gettysburg.wav")
        pygame.mixer.music.queue("music/3-Wildcat.wav")
        pygame.mixer.music.queue("music/4-Loud-Pipes.wav")
        pygame.mixer.music.queue("music/5-Kennedy.wav")
        pygame.mixer.music.queue("music/6-Swisha.wav")
        pygame.mixer.music.queue("music/7-Seventeen-Years.wav")
        pygame.mixer.music.queue("music/8-Desert-Eagle.wav")
        
    def play(self):
        
        pygame.mixer.music.play()
