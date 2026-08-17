from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from entity.collision import collision, collition_pac_gum
from enum_pacman import Menu_name, Direction
from custom_maze import Maze
from entity.player import PlayerDraw
from entity.ghost import GhostBlue, GhostPink, GhostRed, GhostOrange
from entity.pac_gum import PacGum
from texte_zone import Texte

if TYPE_CHECKING:
    from monitor import Monitor


class Game():
    BACKGROUND_COLOR = 119, 51, 68
    TIMER_VULNERABLE = 450

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
                self.maze.maze, (self.maze.height - 1, self.maze.width - 1)),
        ]
        # to-do: change the variable size, for now it s useless...
        self.pac_gum = PacGum((20, 15), self.maze.maze)
        self.txt = Texte(screen, 40, (255, 204, 1))

    def game_loop(
            self,
            monitor: Monitor
          ) -> None:
        # update  logic
        if self.player.dead:
            self.player.pos = self.maze.maze_center
            self.player.direction = Direction.right
            self.player.target = None
            # to-do: opti ?
            self.ghosts = [
                GhostBlue(self.maze.maze, (0, 0)),
                GhostPink(self.maze.maze, (0, self.maze.width - 1)),
                GhostRed(self.maze.maze, (self.maze.height - 1, 0)),
                GhostOrange(
                    self.maze.maze, (self.maze.height-1, self.maze.width-1)),
            ]
            self.player.dead = False

        # update the player (animation)
        key_press = monitor.key_press
        screen_change = monitor.screen_change
        windows_resized = monitor.windows_resized

        if monitor.super_pac_gum:
            monitor.super_pac_gum = False
        self.player.update(key_press)
        for ghost in self.ghosts:
            ghost.update(self.player.pos)

        # Draw
        self.screen.fill(self.BACKGROUND_COLOR)
        if screen_change:
            windows_resized = True
        self.maze.draw(windows_resized)
        cell_size = self.maze.cell_size
        self.pac_gum.draw(
            self.maze.surface,
            cell_size
        )
        for ghost in self.ghosts:
            ghost.draw(
                self.maze.surface,
                cell_size
            )
        self.player.draw(
            self.maze.surface,
            cell_size
        )
        self.txt.display_texte(f"score : {monitor.score}", (0, 0))

        collition_pac_gum(self.player, self.pac_gum, monitor)
        for ghost in self.ghosts:
            if monitor.super_pac_gum:
                ghost.set_vulnerable(self.TIMER_VULNERABLE)
        if collision(
          self.player,
          self.ghosts,
          cell_size,
          monitor,
          self.maze.maze
        ):
            self.player.life -= 1
            self.player.dead = True
            for ghost in self.ghosts:
                ghost.pac_man_dead = True
        if self.player.life <= 0:
            monitor.menu = Menu_name.Reset_game
        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
