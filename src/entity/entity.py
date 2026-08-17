from typing import Optional
from abc import ABC, abstractmethod

import pygame

from enum_packman import Direction


class EntityDraw(ABC):
    FILL_RATIO = 1

    def __init__(
            self,
            cell_size: int
          ) -> None:

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
        pass

    @abstractmethod
    def get_true_pos(self, cell_size: int) -> tuple[float, float]:
        pass


class EntityLogic:
    STEP_BY_CELL = 15

    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int] = (0, 0)
      ) -> None:
        self.pos: tuple[int, int] = start_pos
        self.start_pos = start_pos
        self.maze = maze
        self.direction = Direction.right
        self.target: Optional[tuple[int, int]] = None
        self.delta_movment: int = 0

    def can_go(self, direction: Direction) -> bool:
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
        y, x = map(lambda i: i * cell_size, self.pos)
        if not self.target:
            return y, x

        offset = (cell_size / self.STEP_BY_CELL) * self.delta_movment
        offset_y, offset_x = map(lambda x: x*offset, self.direction.value)

        return y + offset_y, x + offset_x
