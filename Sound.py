import pygame
import random


class Sound:
    def __init__(self):
        pygame.init()
        with open('volume.txt', 'r', encoding='UTF-8') as file:
            var = 50
            for line in file:
                var = int(line.rstrip())
                break
        pygame.mixer.music.load(random.choice(['layouts/necrotic_music.mp3', 'layouts/necrotic_music2.mp3']))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(var / 100)

    def stop(self):
        pygame.mixer.music.stop()