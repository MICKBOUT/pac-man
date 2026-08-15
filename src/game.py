from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from entity.collision import collision, collition_pac_gum
from enum_packman import Menu_name
from custom_maze import Maze
from custom_type import Ghost
from entity.player import PlayerDraw
from entity.ghost import GhostBlue, GhostPink, GhostRed, GhostOrange
from entity.pac_gum import PacGum

if TYPE_CHECKING:
    from monitor import Monitor


class Game():
    BACKGROUND_COLOR = 119, 51, 68

    def __init__(
        self,
        screen: pygame.Surface,
        maze_size: tuple[int, int],
        seed: int = 0,
      ) -> None:
        self.screen = screen
        self.maze = Maze(maze_size, screen, seed)

        self.player = PlayerDraw(
            self.maze.maze,
            self.maze.maze_center,
        )
        self.ghosts = [
            GhostBlue(self.maze.maze, (0, 0)),
            GhostPink(self.maze.maze, (0, self.maze.width - 1)),
            GhostRed(self.maze.maze, (self.maze.height - 1, 0)),
            GhostOrange(
                self.maze.maze, (self.maze.width, self.maze.height - 1)),
        ]
        # to-do: change the variable size, for now it s useless...
        self.pac_gum = PacGum((20, 15), self.maze.maze)

    def game_loop(
            self,
            monitor: Monitor
          ) -> None:
        key_press = monitor.key_press
        screen_change = monitor.screen_change
        windows_resized = monitor.windows_resized

        self.screen.fill(self.BACKGROUND_COLOR)

        self.player.update(key_press)
        for ghost in self.ghosts:
            ghost.update(self.player.pos)

        # draw on the maze rect
        if screen_change:
            windows_resized = True
        self.maze.draw(windows_resized)
        cell_size = None
        if windows_resized:
            cell_size = self.maze.cell_size

        self.pac_gum.draw(
            self.maze.surface,
            cell_size
        )
        self.player.draw(
            self.maze.surface,
            cell_size
        )
        for ghost in self.ghosts:
            ghost.draw(
                self.maze.surface,
                cell_size
            )
        collition_pac_gum(self.player, self.pac_gum)
        if collision(self.player, self.ghosts, cell_size):
            monitor.menu = Menu_name.Reset_game

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
