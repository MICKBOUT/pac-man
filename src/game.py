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
    BACKGROUND_COLOR = 0, 0, 0
    TIMER_VULNERABLE = 450

    def __init__(
        self,
        screen: pygame.Surface,
        maze_size: tuple[int, int],
        monitor: Monitor,
        seed: int = 0
    ) -> None:
        self.screen = screen
        self.maze_size = maze_size
        self.frame_count = 0

        if seed == monitor.config_data.seed:
            self.maze = Maze(maze_size, screen, seed)
        elif monitor.level > len(monitor.config_data.level):
            self.maze = Maze(maze_size, screen, 0)
        else:
            self.maze = Maze(maze_size, screen,
                             monitor.config_data.level[monitor.level])

        self.player = PlayerDraw(
            self.maze.maze,
            self.maze.maze_center,
            monitor.config_data.lives
        )
        self._reset_ghost(monitor)
        # to-do: change the variable size, for now it s useless...
        self.pac_gum = PacGum(self.maze.maze, monitor)
        self.txt = Texte(screen, 40, (255, 204, 1))

        x, y = self.screen.get_size()

    def _reset_ghost(self, monitor: Monitor) -> None:
        self.ghosts = [
            GhostBlue(self.maze.maze, (0, 0), monitor),
            GhostPink(self.maze.maze, (0, self.maze.width - 1), monitor),
            GhostRed(self.maze.maze, (self.maze.height - 1, 0), monitor),
            GhostOrange(
                self.maze.maze, (self.maze.height - 1, self.maze.width - 1),
                monitor
            ),
        ]

    def _game_loop_update(self, monitor: Monitor) -> None:
        self.frame_count += 1
        if monitor.add_life:
            self.player.life += 1
        if monitor.add_timer:
            self.frame_count -= 60 * 10
        if self.player.dead:
            self.player.pos = self.maze.maze_center
            self.player.direction = Direction.right
            self.player.target = None
            self._reset_ghost(monitor)
            self.player.dead = False

        if collision(self.player, self.ghosts, self.maze.cell_size, monitor):
            self.player.life -= 1
            self.player.dead = True
            for ghost in self.ghosts:
                ghost.pac_man_dead = True
        if self.player.life <= 0:
            monitor.level = 0
            monitor.menu = Menu_name.Win

        # update the player (animation)
        if monitor.super_pac_gum:
            monitor.super_pac_gum = False
        self.player.update(monitor.key_press)
        for ghost in self.ghosts:
            ghost.update(self.player.pos)
        if collition_and_win_pacgum(self.player, self.pac_gum, monitor):
            self.frame_count = 0
            monitor.level += 1
            if monitor.level > len(monitor.config_data.level):
                self.maze = Maze(self.maze_size,
                                 self.screen,
                                 0)
            else:
                self.maze = Maze(self.maze_size,
                                 self.screen,
                                 monitor.config_data.level[monitor.level - 1])
            self.pac_gum = PacGum(self.maze.maze, monitor)
            self.player = PlayerDraw(
                        self.maze.maze,
                        self.maze.maze_center,
                        self.player.life
                    )
            self._reset_ghost(monitor)
            monitor.super_pac_gum = False
            if monitor.level >= max(10, len(monitor.config_data.level)):
                monitor.menu = Menu_name.Win
        if monitor.super_pac_gum:
            for ghost in self.ghosts:
                ghost.set_vulnerable(self.TIMER_VULNERABLE)

        if self.frame_count > monitor.config_data.level_max_time * 60:
            monitor.menu = Menu_name.Win

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

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
        self.txt.display_texte(f"score : {monitor.score}", (0, 0))
        self.txt.display_texte(
            "timer : "
            f"{monitor.config_data.level_max_time - self.frame_count // 60}",
            (0, 30)
        )
        self.txt.display_texte(
            "life : "
            f"{self.player.life}",
            (0, 60)
        )

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
