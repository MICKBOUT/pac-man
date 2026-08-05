from enum import Enum


class Menu_name(Enum):
    Menu = 0
    Score = 1
    rules = 2
    Start = 3
    Play = 4


class Txt(Enum):
    Rules = "The objective of Pac-Man is to move through the maze and eat all"\
        " the Pac-Gums while avoiding the ghosts that chase the player. By "\
        "eating the Power Pac-Gums, Pac-Man can temporarily make the ghosts"\
        " vulnerable and eat them for extra points. Bonus fruits also appear"\
        " during the game and provide additional points. A level is completed"\
        " when all the Pac-Gums have been collected, while the game ends if "\
        "Pac-Man loses all of his lives."


class Direction(Enum):
    no_direction = 0
    right = 0, 1
    down = 1, 0
    left = 0, -1
    up = -1, 0
