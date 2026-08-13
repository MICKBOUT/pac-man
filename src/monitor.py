from typing import Optional

import pygame

from validation.validate import ConfigModel
from enum_packman import Menu_name, Direction
from game import Game


class Monitor():
    def __init__(
        self,
        screen: pygame.Surface,
        config_data: ConfigModel
      ) -> None:
        self.windows_resized = False
        self.screen_change = False
        self.key_press: Optional[Direction] = None

        self.game = Game(screen)
        self.config_data: ConfigModel = config_data

        self.menu = Menu_name.Start

        self.register_txt = ""
