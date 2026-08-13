import pygame

from entity.collision import collision
from enum_packman import Menu_name
from custom_maze import Maze
from entity.player import PlayerDraw
from entity.ghost import GhostBlue, GhostPink, GhostRed, GhostOrange


class Game():
    BACKGROUND_COLOR = 119, 51, 68

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.maze = Maze((20, 10), screen)

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
        self.player.update(key_press)
        self.ghost_blue.update()
        self.ghost_pink.update(self.player.pos)
        self.ghost_red.update(self.player.pos)
        self.ghost_orange.update()

        # draw on the maze rect
        if screen_change:
            windows_resized = True
        self.maze.draw(windows_resized)
        cell_size = None
        if windows_resized:
            cell_size = self.maze.cell_size

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
        if collision(self.player, [
            self.ghost_blue,
            self.ghost_pink,
            self.ghost_red,
            self.ghost_orange
            ], cell_size
          ):
            monitor.menu = Menu_name.Reset_game.value

        # draw the maze on the screen
        self.screen.blit(self.maze.surface, self.maze.rect.topleft)
