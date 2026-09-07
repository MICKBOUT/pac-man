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


class Game:
    """Encapsulates game state and the main update/draw loop.

    Attributes:
        BACKGROUND_COLOR: Background color for the game screen.
        TIMER_VULNERABLE: Number of frames a ghost remains vulnerable.
    """

    BACKGROUND_COLOR = 0, 0, 0
    TIMER_VULNERABLE = 375

    def __init__(
        self,
        screen: pygame.Surface,
        maze_size: tuple[int, int],
        monitor: Monitor,
        seed: int = 0
    ) -> None:
        """Initialize game components for the provided screen/maze size.

        Args:
            screen: `pygame.Surface` to draw the game into.
            maze_size: Tuple `(height, width)` used to generate the maze.
            monitor: A `Monitor` instance providing configuration and input
                state used by the game loop.
            seed: Optional seed value used to select or generate maze data.
        """
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
        """Instantiate and position the four ghost entities.

        Args:
            monitor: Monitor used to propagate resize/debug flags.
        """
        self.ghosts = [
            GhostBlue(self.maze.maze, (0, 0), monitor),
            GhostPink(self.maze.maze, (0, self.maze.width - 1), monitor),
            GhostRed(self.maze.maze, (self.maze.height - 1, 0), monitor),
            GhostOrange(
                self.maze.maze, (self.maze.height - 1, self.maze.width - 1),
                monitor
            ),
        ]
        monitor.resize_entity = True

    def _game_loop_update(self, monitor: Monitor) -> None:
        """Advance game state by a single tick.

        This updates timers, applies player input, advances all entity
        logic, checks collisions, awards points for pac-gum collection,
        and handles level progression or game-over transitions by mutating
        the provided `monitor`.

        Args:
            monitor: The game's `Monitor` instance providing input/state.
        """
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
        """Render the current game state to the screen surface.

        The method draws the maze, pac-gums, ghosts and player, and shows
        HUD information such as score, timer and lives.

        Args:
            monitor: The game's `Monitor` instance providing flags used to
                determine whether assets need resizing for the current
                screen dimensions.
        """
        need_resize = monitor.windows_resized or monitor.resize_entity
        monitor.resize_entity = False

        self.screen.fill(self.BACKGROUND_COLOR)

        self.maze.draw(need_resize)
        self.pac_gum.draw(
            self.maze.surface,
            self.maze.cell_size
        )
        for ghost in self.ghosts:
            if need_resize:
                ghost.draw(self.maze.surface, self.maze.cell_size)
            else:
                ghost.draw(self.maze.surface)
        if need_resize:
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
        """Single-frame entry point: update then draw.

        Args:
            monitor: The `Monitor` instance providing input and state.
        """

        self._game_loop_update(monitor)
        self._game_loop_draw(monitor)

    def pause_loop(
        self,
        monitor: Monitor,
      ) -> None:
        """Render a paused overlay while still drawing the current frame.

        This draws the current game frame with a semi-transparent black
        overlay and a centered rectangle to indicate the paused state.

        Args:
            monitor: The `Monitor` instance providing `screen_size`.
        """

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
