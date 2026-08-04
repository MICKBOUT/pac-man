from enum import Enum


class Menu_name(Enum):
    Menu = 0
    Score = 1
    rules = 2
    Start = 3
    Play = 4


class Direction(Enum):
    no_direction = 0
    right = 0, 1
    down = 1, 0
    left = 0, -1
    up = -1, 0
