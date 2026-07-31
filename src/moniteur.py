from enum_packman import Menu_name
import custom_maze
from player import Player


class Moniteur():
    def __init__(self, windows):
        self.menu = Menu_name.Start.value
        self.maze = custom_maze.Maze((20, 20), windows.get_size())
        self.pacman = Player(self.maze.cell_size)
