import pygame

from custom_maze import Maze
from player import PlayerDraw, PlayerLogic


class Game():
    BACKGROUND_COLOR = 119, 51, 68

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.maze = Maze((20, 20), screen)
        self.player_draw = PlayerDraw()
        self.Player_logic = PlayerLogic(
            start_pos=self.maze.maze_center
        )

    def game_loop(
            self,
            windows_resized: bool = False,
            screen_change: bool = False
          ) -> None:
        # empty the last screen by filling the screen
        self.screen.fill(self.BACKGROUND_COLOR)

        # update the player (animation)
        self.Player_logic.update()
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
            self.Player_logic.pos,
            cell_size
        )

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
