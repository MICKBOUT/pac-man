from typing import Optional

import pygame

from validation.validate import ConfigModel
from enum_pacman import Menu_name, Direction
from game import Game
from register import takeHeightScore


class Monitor():
    def __init__(
        self,
        screen: pygame.Surface,
        config_data: ConfigModel,
      ) -> None:
        self.windows_resized = False
        self.screen_change = False
        self.super_pac_gum = False
        self.esp = False
        self.score = 0
        self.register_txt = ""
        self.key_press: Optional[Direction] = None
        self.menu: Menu_name = Menu_name.Start
        self.config_data: ConfigModel = config_data
        self.score = 0
        self.level = 0
        self.super_pac_gum = False
        self.height_score = takeHeightScore(
            config_data.highscore_filename
            )
        self.game = Game(
            screen,
            (config_data.width, config_data.height),
            self,
            config_data.seed
        )
        self.screen_size = (1280, 720)  # defalut value, change at execution
