import pygame

from custom_maze import Maze
from player import Player


class Game():
    BACKGROUND_COLOR = 119, 51, 68

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.maze = Maze((20, 20), screen)
        self.pacman = Player()

    def game_loop(
            self,
            windows_resized: bool = False,
            screen_change: bool = False
          ) -> None:
        # empty the last screen by filling the screen
        self.screen.fill(self.BACKGROUND_COLOR)

        # update the player
        self.pacman.update()

        # draw on the maze rect
        if screen_change:
            windows_resized = True
        self.maze.draw(windows_resized)
        if windows_resized:
            self.pacman.draw(self.maze.surface, self.maze.cell_size)
        else:
            self.pacman.draw(self.maze.surface)

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
