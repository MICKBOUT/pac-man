from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from entity.collision import collision, collition_pac_gum
from enum_packman import Menu_name
from custom_maze import Maze
from entity.player import PlayerDraw, Direction
from entity.ghost import GhostBlue, GhostPink, GhostRed, GhostOrange
from entity.pac_gum import PacGum
from texte_zone import Texte

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
        self.ghost_blue = GhostBlue(self.maze.maze, (0, 0))
        self.ghost_pink = GhostPink(
            self.maze.maze, (0, len(self.maze.maze[0]) - 1)
        )
        self.ghost_red = GhostRed(
            self.maze.maze, (len(self.maze.maze) - 1, 0)
        )
        self.ghost_orange = GhostOrange(
            self.maze.maze,
            (len(self.maze.maze) - 1, len(self.maze.maze[0]) - 1)
        )
        self.pac_gum = PacGum((20, 15), self.maze.maze)
        self.txt = Texte(screen, 40, (255, 204, 1))

    def game_loop(
            self,
            monitor: Monitor
          ) -> None:
        if self.player.dead:
            self.player.pos = self.maze.maze_center
            self.player.direction = Direction.right
            self.player.target = []
            self.ghost_blue.reset()
            self.ghost_red.reset()
            self.ghost_orange.reset()
            self.ghost_pink.reset()
            self.player.dead = False

        key_press = monitor.key_press
        screen_change = monitor.screen_change
        windows_resized = monitor.windows_resized
        # empty the last screen by filling the screen
        self.screen.fill(self.BACKGROUND_COLOR)

        # update the player (animation)
        if monitor.super_pac_gum:
            monitor.super_pac_gum = False
        self.player.update(key_press)
        self.ghost_blue.update(self.player.pos)
        self.ghost_pink.update(self.player.pos)
        self.ghost_red.update(self.player.pos)
        self.ghost_orange.update(self.player.pos)

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
        self.ghost_blue.draw(
            self.maze.surface,
            cell_size
        )
        self.ghost_pink.draw(
            self.maze.surface,
            cell_size
        )
        self.ghost_red.draw(
            self.maze.surface,
            cell_size
        )
        self.ghost_orange.draw(
            self.maze.surface,
            cell_size
        )
        self.txt.display_texte(f"score : {monitor.score}", (0, 0))
        collition_pac_gum(self.player,
                          self.pac_gum,
                          monitor)
        if monitor.super_pac_gum:
            self.ghost_blue.set_vulnerable(300)
            self.ghost_pink.set_vulnerable(300)
            self.ghost_red.set_vulnerable(300)
            self.ghost_orange.set_vulnerable(300)

        if collision(self.player, [
            self.ghost_blue,
            self.ghost_pink,
            self.ghost_red,
            self.ghost_orange
            ], cell_size,
            monitor,
            self.maze.maze
          ):
            self.player.life -= 1
            self.player.dead = True
            self.ghost_blue.pac_man_dead = True
            self.ghost_orange.pac_man_dead = True
            self.ghost_pink.pac_man_dead = True
            self.ghost_red.pac_man_dead = True
        if self.player.life <= 0:
            monitor.menu = Menu_name.Reset_game
        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
