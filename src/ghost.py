import random
from typing import Optional

import pygame

from enum_packman import Direction


class GhostDraw():
    FILL_RATIO = 1
    IMAGES_PATHS = [
        "assets/animation/blue_gost/1.png",
        "assets/animation/blue_gost/2.png"
    ]

    def __init__(self, ghost: GhostLogic, cell_size: int = 15) -> None:
        self.ghost = ghost

        self.images_loaded = [
            pygame.image.load(path).convert_alpha()
            for path in self.IMAGES_PATHS
        ]

        self.cell_size = cell_size
        self.ghost_assets = []
        self._reszie_img()

        self.image: pygame.Surface = self.ghost_assets[0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))
        self.internal_counter = 0

    def _reszie_img(self) -> None:
        self.ghost_assets = [
            pygame.transform.scale(
                image,
                (
                    int(self.cell_size * self.FILL_RATIO),
                    int(self.cell_size * self.FILL_RATIO)
                )
            )
            for image in self.images_loaded
        ]

    def update(self) -> None:
        self.internal_counter += 1

    def draw(
            self,
            surface: pygame.Surface,
            cell_resized: Optional[int] = None
          ) -> None:
        if cell_resized:
            self.cell_size = cell_resized
            self._reszie_img()

        surface.blit(
            self.ghost_assets[
                (self.internal_counter // 5) % len(self.ghost_assets)
            ],
            (
                self.ghost.get_true_pos(self.cell_size),
                self.rect.size
            ),
        )


class GhostLogic():
    STEP_BY_CELL = 13

    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int] = (0, 0)
      ) -> None:
        self.pos = list(start_pos)
        self.maze = maze
        self.direction = Direction.right
        self.target = None

    # to-do: this methode is a duplice, maybe create a common classe
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

    # to-do: same as above
    def get_true_pos(self, cell_size: int) -> tuple[int, int]:
        y, x = map(lambda x: x * cell_size, self.pos)
        if self.target is None:
            return y, x

        offset = (cell_size / self.STEP_BY_CELL) * self.delta_movment
        offset_y, offset_x = map(lambda x: x*offset, self.direction.value)

        return y + offset_y, x + offset_x

    def update(self) -> None:
        if self.target is None:
            self.direction = random.choice([
                direction for direction in [
                    Direction.left, Direction.up,
                    Direction.down, Direction.right
                ]
                if self.can_go(direction)
            ])
            dir_y, dir_x = self.direction.value
            self.target = [self.pos[0] + dir_y, self.pos[1] + dir_x]
            self.delta_movment = 0

        if self.target is not None:
            self.delta_movment += 1
            if self.delta_movment >= self.STEP_BY_CELL:
                self.pos = self.target
                self.target = None
                self.delta_movment = 0
