# mypy: disable-error-code="unused-ignore"

import pygame

import mazegenerator  # type: ignore[import-untyped]


class Maze(mazegenerator.MazeGenerator):  # type: ignore[misc]
    """Maze renderer that draws walls and optional logo cells.

    Constants:
        MAZE_BACKGROUND_COLOR: Background color for the maze surface.
        CELL_WALL_COLOR: Color used to draw wall segments.
        COLOR_LOGO: Color used to fill special logo cells (wall==15).
    """

    MAZE_BACKGROUND_COLOR = 11, 0, 20
    CELL_WALL_COLOR = 245, 233, 226
    COLOR_LOGO = 232, 241, 242

    def __init__(
        self,
        maze_size: tuple[int, int],
        screen: pygame.Surface,
        seed: int = 0,
    ):
        """Create a `Maze` renderer and prepare the drawing surface.

        Args:
            maze_size: (height, width) tuple for the generated maze.
            screen: `pygame.Surface` used to determine available screen size
                and blit the resulting maze surface.
            seed: Optional RNG seed forwarded to the generator.
        """
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
        """Draw a single cell at pixel offset `(offset_x, offset_y)`.

        The `wall` integer encodes which cell edges contain walls. When
        `wall == 15` the cell is treated as a filled logo cell and drawn
        as a rectangle using `COLOR_LOGO`.

        Args:
            wall: Integer encoding wall segments for the cell.
            offset_x: X pixel offset within the maze surface.
            offset_y: Y pixel offset within the maze surface.
        """

        if wall == 15:
            pygame.draw.rect(
                self.surface, self.COLOR_LOGO, (
                    (offset_x, offset_y),
                    (self.cell_size, self.cell_size)
                )
            )
            return

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
        """Compute sizes and create an appropriately sized surface.

        The method calculates `cell_size` so the maze fits within the
        available `screen` area and prepares `pos_first_cell`, `rect` and
        the backing `surface` used for drawing the maze.
        """
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

    def draw(self, need_resize: bool) -> None:
        """Draw the entire maze onto the internal surface.

        Args:
            need_resize: When True recompute the sizes before drawing.
        """

        if need_resize:
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
