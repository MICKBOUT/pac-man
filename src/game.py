from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from entity.collision import collision, collition_and_win_pacgum
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
        monitor: Monitor,
        seed: int = 0
    ) -> None:
        self.screen = screen
        self.maze = Maze(maze_size, screen, seed)
        self.player = PlayerDraw(
            self.maze.maze,
            self.maze.maze_center,
        )
        self.ghosts = [
            GhostBlue(self.maze.maze, (0, 0), monitor),
            GhostPink(self.maze.maze, (0, self.maze.width - 1), monitor),
            GhostRed(self.maze.maze, (self.maze.height - 1, 0), monitor),
            GhostOrange(
                self.maze.maze, (self.maze.height - 1, self.maze.width - 1),
                monitor
            ),
        ]
        # to-do: change the variable size, for now it s useless...
        self.pac_gum = PacGum((20, 15), self.maze.maze, monitor)
        self.txt = Texte(screen, 40, (255, 204, 1))

        x, y = self.screen.get_size()

    def _game_loop_update(self, monitor):
        if self.player.dead:
            self.player.pos = self.maze.maze_center
            self.player.direction = Direction.right
            self.player.target = None
            # to-do: opti ?
            self.ghosts = [
                GhostBlue(self.maze.maze, (0, 0), monitor),
                GhostPink(self.maze.maze, (0, self.maze.width - 1), monitor),
                GhostRed(self.maze.maze, (self.maze.height - 1, 0), monitor),
                GhostOrange(
                    self.maze.maze,
                    (self.maze.height - 1, self.maze.width - 1), monitor),
            ]
            self.player.dead = False

        if collision(self.player, self.ghosts, self.maze.cell_size, monitor):
            self.player.life -= 1
            self.player.dead = True
            for ghost in self.ghosts:
                ghost.pac_man_dead = True
        if self.player.life <= 0:
            monitor.menu = Menu_name.Win

        # update the player (animation)
        if monitor.super_pac_gum:
            monitor.super_pac_gum = False
        self.player.update(monitor.key_press)
        for ghost in self.ghosts:
            ghost.update(self.player.pos)
        if collition_and_win_pacgum(self.player, self.pac_gum, monitor):
            monitor.menu = Menu_name.Win
        for ghost in self.ghosts:
            if monitor.super_pac_gum:
                ghost.set_vulnerable(self.TIMER_VULNERABLE)

    def _game_loop_draw(self, monitor: Monitor) -> None:
        screen_change = monitor.screen_change
        windows_resized = monitor.windows_resized
        if screen_change:
            windows_resized = True

        self.screen.fill(self.BACKGROUND_COLOR)

        self.maze.draw(windows_resized)
        self.pac_gum.draw(
            self.maze.surface,
            self.maze.cell_size
        )
        for ghost in self.ghosts:
            if windows_resized:
                ghost.draw(self.maze.surface, self.maze.cell_size)
            else:
                ghost.draw(self.maze.surface)
        if windows_resized:
            self.player.draw(self.maze.surface, self.maze.cell_size)
        else:
            self.player.draw(self.maze.surface)
        self.txt.display_texte(f"score : {monitor.score}", (0, 0))

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)

    def game_loop(
            self,
            monitor: Monitor
          ) -> None:

        self._game_loop_update(monitor)
        self._game_loop_draw(monitor)

    def pause_loop(
        self,
        monitor: Monitor,
      ) -> None:

        alpha_screen = pygame.Surface(monitor.screen_size).convert()
        alpha_screen.fill((0, 0, 0))
        alpha_screen.set_alpha(128)

        screen_width, screen_height = self.screen.get_size()
        self._game_loop_draw(monitor)
        self.screen.blit(alpha_screen, (0, 0))
        pygame.draw.rect(
            self.screen,
            (0, 0, 0, 128), (
                (screen_width // 4, screen_height // 4),
                (screen_width // 2, screen_height // 2)
            )
        )
