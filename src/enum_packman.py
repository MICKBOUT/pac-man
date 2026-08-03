from enum import Enum


class Menu_name(Enum):
    Menu = 0
    Score = 1
    rules = 2
    Start = 3
    Play = 4


class Direction(Enum):
    no_direction = 0
    right = 1
    down = 2
    left = 3
    up = 4
