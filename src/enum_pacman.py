"""Shared enums used across the game.

This module provides a small set of enumerations used for menu state
selection, long text constants, and movement `Direction` values. The
`Direction` enum stores `(dy, dx)` tuples suitable for grid-based
movement offsets.
"""

from enum import Enum


class Menu_name(Enum):
    """Names for various menu/screens in the game.

    Members correspond to the high-level UI states used by the menu
    and game controller.
    """

    Menu = 0
    Score = 1
    Rules = 2
    Start = 3
    Play = 4
    Register = 5
    Reset_game = 6
    Win = 7
    Game_pause = 8


class Txt(Enum):
    """Container for long text constants.

    The `Rules` member contains the game rules/help text shown in the
    rules screen.
    """

    Rules = "The objective of Pac-Man is to move through the maze and eat all"\
        " the Pac-Gums while avoiding the ghosts that chase the player. By "\
        "eating the Power Pac-Gums, Pac-Man can temporarily make the ghosts"\
        " vulnerable and eat them for extra points. Bonus fruits also appear"\
        " during the game and provide additional points. A level is completed"\
        " when all the Pac-Gums have been collected, while the game ends if "\
        "Pac-Man loses all of his lives."


class Direction(Enum):
    """Cardinal directions encoded as `(dy, dx)` offsets.

    The tuple value for each enum member represents the change to apply to
    a grid coordinate `(y, x)` when moving one cell in that direction.
    """

    no_direction = 0, 0
    right = 0, 1
    down = 1, 0
    left = 0, -1
    up = -1, 0
