import pygame

import mazegenerator


class Maze(mazegenerator.MazeGenerator):
    MAZE_BACKGROUND_COLOR = 11, 0, 20
    CELL_WALL_COLOR = 245, 233, 226

    def __init__(
        self,
        size: tuple[int, int],
        screen_size: tuple[int, int],
        seed: int = 0,
    ):
        super().__init__(size, seed=seed)
        screen_width, screen_height = screen_size

        self.maze_height, self.maze_width = len(self.maze), len(self.maze[0])
        self.cell_size = min(
            (screen_height - 10) // self.maze_height,
            (screen_width - 10) // self.maze_width,
        )

        center_x, center_y = screen_width // 2, screen_height // 2
        self.pos_first_cell = (
            center_x - (self.maze_width * self.cell_size // 2),
            center_y - (self.maze_height * self.cell_size // 2)
        )

        self.rect = pygame.Rect(
            self.pos_first_cell,
            (
                self.maze_width * self.cell_size + 1,
                self.maze_height * self.cell_size + 1
            ),
        )

        self.surface = pygame.Surface(self.rect.size)

    def __draw_cell(
        self,
        wall: int,
        offset_x: int,
        offset_y: int,
    ):

        # North
        if wall % 2:
            pygame.draw.line(
                self.surface,
                self.CELL_WALL_COLOR,
                (offset_x, offset_y),
                (offset_x + self.cell_size, offset_y)
            )
        # East
        wall //= 2
        if wall % 2:
            pygame.draw.line(
                self.surface,
                self.CELL_WALL_COLOR,
                (offset_x + self.cell_size, offset_y),
                (offset_x + self.cell_size, offset_y + self.cell_size)
            )
        # South
        wall //= 2
        if wall % 2:
            pygame.draw.line(
                self.surface,
                self.CELL_WALL_COLOR,
                (offset_x, offset_y + self.cell_size),
                (offset_x + self.cell_size, offset_y + self.cell_size)
            )
        # West
        wall //= 2
        if wall % 2:
            pygame.draw.line(
                self.surface,
                self.CELL_WALL_COLOR,
                (offset_x, offset_y),
                (offset_x, offset_y + self.cell_size)
            )

    def draw(self):
        start_x, start_y = self.pos_first_cell
        pygame.draw.rect(
            self.surface,
            self.MAZE_BACKGROUND_COLOR,
            (
                (0, 0),
                (
                    self.maze_width * self.cell_size,
                    self.maze_height * self.cell_size
                )
            ),
        )

        for y, line in enumerate(self.maze):
            for x, cell in enumerate(line):
                self.__draw_cell(
                    cell,
                    x * self.cell_size,
                    y * self.cell_size,
                )
