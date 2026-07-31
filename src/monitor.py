import pygame

from enum_packman import Menu_name
from game import Game


class Monitor():
    def __init__(self, screen: pygame.Surface):
        self.windows_resized = False
        self.screen_change = False

        self.menu = Menu_name.Start.value
        self.game = Game(screen)
