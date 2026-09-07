from typing import Optional

import pygame

from validation.validate import ConfigModel
from enum_pacman import Menu_name, Direction
from game import Game
from register import takeHeightScore


class Monitor:
    """Container for application-wide runtime state.

    Attributes:
        add_life: Whether a life should be added on next update.
        add_timer: Whether a timer event is pending.
        windows_resized: Set when the window size changed.
        resize_entity: Flag to indicate entities should be resized.
        super_pac_gum: Whether super pac-gum mode is active.
        esp: Miscellaneous debug/cheat flag.
        score: Current player score.
        register_txt: Temporary text buffer for registration input.
        key_press: Last received direction key or None.
        menu: Current `Menu_name` value.
        config_data: Loaded `ConfigModel` configuration.
        level: Current game level.
        height_score: High-score list loaded from disk.
        game: Active `Game` instance.
        screen_size: Default screen size tuple.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        config_data: ConfigModel,
    ) -> None:
        """Initialize monitor state and construct the `Game`.

        Args:
            screen: `pygame.Surface` used as the game's render target.
            config_data: Validated `ConfigModel` containing settings.

        Raises:
            Exception: Re-raises exceptions originating from loading the
                high-score file via `takeHeightScore`.
        """
        self.add_life = False
        self.add_timer = False
        self.windows_resized = False
        self.resize_entity = False
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
        try:
            self.height_score = takeHeightScore(
                config_data.highscore_filename
            )
        except Exception as m:
            raise Exception(m)
        self.game = Game(
            screen,
            (config_data.width, config_data.height),
            self,
            config_data.seed,
        )
        self.screen_size = (1280, 720)  # default value, changed at runtime
