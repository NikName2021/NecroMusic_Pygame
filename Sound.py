import pygame
import random


class Sound:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load(random.choice(['layouts/necrotic_music.mp3', 'layouts/necrotic_music2.mp3']))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)

    def stop(self):
        pygame.mixer.music.stop()