from typing import Optional
from abc import ABC, abstractmethod

import pygame

from enum_pacman import Direction


class EntityDraw(ABC):
    """Abstract base class for drawable entities.

    Attributes:
        cell_size: Size (in pixels) of a single grid cell used for rendering.
        internal_frame_counter: Counter for animation frame selection.
        direction: Current `Direction` used to select animation assets.
        assets: Mapping from `Direction` to a list of `pygame.Surface` frames.
        nb_frame: Number of frames available for the current animation.
        image: Current `pygame.Surface` used when measuring entity bounds.
        rect: `pygame.Rect` of the current `image` used for blitting.

    Note:
        Subclasses must implement `_reszie_img` and `get_true_pos`.
    """

    def __init__(
            self,
            cell_size: int
          ) -> None:
        """Initialize rendering-related state for the entity.

        Args:
            cell_size: Pixel size of a single map cell used to size assets.
        """

        self.cell_size = cell_size

        self.internal_frame_counter = 0

        self.direction = Direction.no_direction
        self.assets: dict[Direction, list[pygame.Surface]] = {}
        self._reszie_img()
        self.nb_frame = len(self.assets[Direction.right])
        self.image: pygame.Surface = self.assets[Direction.right][0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))

    def draw(
            self,
            surface: pygame.Surface,
            cell_resized: Optional[int] = None
          ) -> None:
        """Render the entity on the provided surface.

        The method optionally accepts a `cell_resized` value to update the
        internal `cell_size` and resize image assets accordingly. The current
        animation frame is selected based on `internal_frame_counter`.

        Args:
            surface: The `pygame.Surface` to draw onto.
            cell_resized: Optional new cell size to apply before drawing.
        """
        if cell_resized:
            self.cell_size = cell_resized
            self._reszie_img()
        self.internal_frame_counter += 1

        true_y, true_x = self.get_true_pos(self.cell_size)
        try:
            surface.blit(
                self.assets[self.direction][
                    (self.internal_frame_counter // 5) % self.nb_frame
                ],
                (
                    (true_x, true_y),
                    self.rect.size
                ),
            )
        except KeyError:
            pass

    @abstractmethod
    def _reszie_img(self) -> None:
        """Resize or populate `self.assets` according to `self.cell_size`.

        Implementations should prepare `self.assets` for each `Direction` and
        ensure at least `Direction.right` is available for sizing and rect
        measurement.
        """
        pass

    @abstractmethod
    def get_true_pos(self, cell_size: int) -> tuple[float, float]:
        """Return the pixel (y, x) position used for rendering.

        Args:
            cell_size: Current cell size (pixels) used to compute offsets.

        Returns:
            A tuple `(y, x)` with the top-left pixel coordinates for drawing.
        """
        pass


class EntityLogic:
    """Grid-based movement and utility state for an entity.

    Attributes:
        STEP_BY_CELL: Number of sub-steps used when interpolating movement.
        pos: Current grid `(y, x)` cell coordinates.
        start_pos: Initial starting position (grid coordinates).
        maze: 2D list representing the maze; used to determine valid moves.
        direction: Current `Direction` for movement.
        target: Optional target grid cell while moving.
        delta_movment: Integer progress toward `target` in sub-steps.
    """

    STEP_BY_CELL = 15

    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int] = (0, 0)
      ) -> None:
        """Initialize logic state for grid movement.

        Args:
            maze: 2D integer matrix describing walkable directions per cell.
            start_pos: Optional initial `(y, x)` position for the entity.
        """
        self.pos: tuple[int, int] = start_pos
        self.start_pos = start_pos
        self.maze = maze
        self.direction = Direction.right
        self.target: Optional[tuple[int, int]] = None
        self.delta_movment: int = 0

    def can_go(self, direction: Direction) -> bool:
        """Return whether movement in `direction` is allowed from `pos`.

        The maze encoding uses bit flags per cell; this function decodes the
        appropriate bit for each direction and returns True if the path is
        open.

        Args:
            direction: The `Direction` to test for movement availability.

        Returns:
            True if the entity can move in the requested direction.
        """
        y, x = self.pos
        match direction:
            case Direction.right:
                return ((self.maze[y][x] // 2) % 2 == 0)
            case Direction.down:
                return ((self.maze[y][x] // 4) % 2 == 0)
            case Direction.left:
                return ((self.maze[y][x] // 8) % 2 == 0)
            case Direction.up:
                return (self.maze[y][x] % 2 == 0)
            case _:
                return False

    def get_true_pos(self, cell_size: int) -> tuple[float, float]:
        """Compute the interpolated pixel position for the current grid `pos`.

        If `target` is set, returns an interpolated position between `pos`
        and `target` based on `delta_movment` and `STEP_BY_CELL`.

        Args:
            cell_size: Pixel size of a single map cell.

        Returns:
            Tuple `(y, x)` with the pixel coordinates for the entity.
        """
        y, x = map(lambda i: i * cell_size, self.pos)
        if not self.target:
            return y, x

        offset = (cell_size / self.STEP_BY_CELL) * self.delta_movment
        offset_y, offset_x = map(lambda x: x*offset, self.direction.value)

        return y + offset_y, x + offset_x
