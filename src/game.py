import pygame

from entity.collision import collision
from enum_packman import Menu_name
from custom_maze import Maze
from entity.player import PlayerDraw, PlayerLogic
from entity.ghost import GhostLogic, GhostDraw, target_cell_blue_ghost


class Game():
    BACKGROUND_COLOR = 119, 51, 68

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.maze = Maze((20, 10), screen)
        self.player_logic = PlayerLogic(self.maze.maze, self.maze.maze_center)
        self.player_draw = PlayerDraw(self.player_logic)

        self.ghost_logic_blue = GhostLogic(
            self.maze.maze,
            target_cell_algo=target_cell_blue_ghost
        )
        self.ghost_draw_blue = GhostDraw(self.ghost_logic_blue)

    def game_loop(
            self,
            monitor
          ) -> None:
        key_press = monitor.key_press
        screen_change = monitor.screen_change
        windows_resized = monitor.windows_resized
        # empty the last screen by filling the screen
        self.screen.fill(self.BACKGROUND_COLOR)

        # update the player (animation)
        self.player_logic.update(key_press)
        self.ghost_logic_blue.update()
        self.player_draw.update()

        # draw on the maze rect
        if screen_change:
            windows_resized = True
        self.maze.draw(windows_resized)
        cell_size = None
        if windows_resized:
            cell_size = self.maze.cell_size

        self.player_draw.draw(
            self.maze.surface,
            cell_size
        )
        self.ghost_draw_blue.draw(
            self.maze.surface,
            cell_size
        )
        if collision(self.player_logic, [self.ghost_logic_blue], cell_size):
            monitor.menu = Menu_name.Menu.value

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
