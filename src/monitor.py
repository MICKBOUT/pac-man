from typing import Optional

import pygame

from enum_packman import Menu_name, Direction
from game import Game


class Monitor():
    def __init__(self, screen: pygame.Surface):
        self.windows_resized = False
        self.screen_change = False
        self.key_press: Optional[Direction] = None

        self.menu = Menu_name.Start.value
        self.game = Game(screen)

        self.register_txt = ""
