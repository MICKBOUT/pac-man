# mypy: disable-error-code="unused-ignore"

import pygame

import mazegenerator  # type: ignore[import-untyped]


class Maze(mazegenerator.MazeGenerator):  # type: ignore[misc]
    MAZE_BACKGROUND_COLOR = 11, 0, 20
    CELL_WALL_COLOR = 245, 233, 226

    def __init__(
        self,
        maze_size: tuple[int, int],
        screen: pygame.Surface,
        seed: int = 0,
    ):
        super().__init__(maze_size, seed=seed)
        self.height, self.width = len(self.maze), len(self.maze[0])
        self.maze_center = (
            (self.height - 1) // 2,
            (self.width - 1) // 2
        )

        self.screen = screen

        self._resize_screen()

    def _draw_cell(
        self,
        wall: int,
        offset_x: int,
        offset_y: int,
    ) -> None:

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

    def _resize_screen(self) -> None:
        screen_width, screen_height = self.screen.get_size()
        self.cell_size = min(
            (screen_height - 50) // self.height,
            (screen_width - 275) // self.width,
        )

        self.pos_first_cell = (
            screen_width // 2 - (self.width * self.cell_size // 2),
            screen_height // 2 - (self.height * self.cell_size // 2)
        )

        self.rect = pygame.Rect(
            self.pos_first_cell,
            (
                self.width * self.cell_size + 1,
                self.height * self.cell_size + 1
            ),
        )

        self.surface = pygame.Surface(self.rect.size)

    def draw(self, windows_resized: bool) -> None:

        if windows_resized:
            self._resize_screen()

        start_x, start_y = self.pos_first_cell
        pygame.draw.rect(
            self.surface,
            self.MAZE_BACKGROUND_COLOR,
            (
                (0, 0),
                (
                    self.width * self.cell_size,
                    self.height * self.cell_size
                )
            ),
        )

        for y, line in enumerate(self.maze):
            for x, cell in enumerate(line):
                self._draw_cell(
                    cell,
                    x * self.cell_size,
                    y * self.cell_size,
                )
