import pygame


class Sound:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('layouts/necrotic_music.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)

    def stop(self):
        pygame.mixer.music.stop()