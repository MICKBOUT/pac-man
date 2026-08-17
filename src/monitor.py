from typing import Optional

import pygame

from validation.validate import ConfigModel
from enum_pacman import Menu_name, Direction
from game import Game


class Monitor():
    def __init__(
        self,
        screen: pygame.Surface,
        config_data: ConfigModel,
      ) -> None:
        self.windows_resized = False
        self.screen_change = False
        self.key_press: Optional[Direction] = None
        self.menu: Menu_name = Menu_name.Start
        self.register_txt = ""
        self.config_data: ConfigModel = config_data
        self.game = Game(
            screen,
            (config_data.width, config_data.height),
            config_data.seed
        )
        self.score = -10
        self.super_pac_gum = False
