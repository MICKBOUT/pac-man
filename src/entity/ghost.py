import random
from abc import ABC, abstractmethod

import pygame

from entity.entity import EntityLogic, EntityDraw
from entity.solver import solver_heap
from enum_packman import Direction
from entity.solver import MisplaceCell


class GhostDraw(EntityDraw):
    IMAGES_PATHS = {
        Direction.right: [
            "assets/ghost/blue/blue_ghost_right_1.png",
            "assets/ghost/blue/blue_ghost_right_2.png"
        ],
        Direction.down: [
            "assets/ghost/blue/blue_ghost_down_1.png",
            "assets/ghost/blue/blue_ghost_down_2.png",
        ],
        Direction.left: [
            "assets/ghost/blue/blue_ghost_left_1.png",
            "assets/ghost/blue/blue_ghost_left_2.png",
        ],
        Direction.up: [
            "assets/ghost/blue/blue_ghost_up_1.png",
            "assets/ghost/blue/blue_ghost_up_2.png",
        ]
    }

    def __init__(self, ghost: GhostLogic, cell_size: int = 15) -> None:
        self.images_loaded = {
            key: [
                pygame.image.load(path).convert_alpha()
                for path in value
            ]
            for key, value in self.IMAGES_PATHS.items()
        }
        super().__init__(ghost, cell_size)

    def _reszie_img(self) -> None:
        self.assets = {
            key: [pygame.transform.scale(
                image, (
                    int(self.cell_size * self.FILL_RATIO),
                    int(self.cell_size * self.FILL_RATIO)
                    )
                )
                for image in value
            ]
            for key, value in self.images_loaded.items()
        }


class GhostLogic(EntityLogic, ABC):
    def __init__(self, maze: list[list[int]]) -> None:
        super().__init__(maze)
        self.target_cell: list[Direction] | None = None
        self.step: int = 0
        self.new_target_cell(maze, self.pos)

    @abstractmethod
    def new_target_cell(self) -> None:
        pass

    def update(self) -> None:
        if self.target is None:
            assert self.target_cell is not None
            self.direction = self.target_cell[self.step]
            dir_y, dir_x = self.direction.value
            self.target = [self.pos[0] + dir_y, self.pos[1] + dir_x]
            self.delta_movment = 0

        if self.target is not None:
            self.delta_movment += 1
            if self.delta_movment >= self.STEP_BY_CELL:
                self.pos = self.target
                self.target = None
                self.delta_movment = 0
                self.step += 1
                assert self.target_cell is not None
                if self.step >= len(self.target_cell):
                    self.new_target_cell(self.maze, self.pos)


class GhostBlue(GhostLogic):
    IMAGES_PATHS = {
        Direction.right: [
            "assets/ghost/blue/blue_ghost_right_1.png",
            "assets/ghost/blue/blue_ghost_right_2.png"
        ],
        Direction.down: [
            "assets/ghost/blue/blue_ghost_down_1.png",
            "assets/ghost/blue/blue_ghost_down_2.png",
        ],
        Direction.left: [
            "assets/ghost/blue/blue_ghost_left_1.png",
            "assets/ghost/blue/blue_ghost_left_2.png",
        ],
        Direction.up: [
            "assets/ghost/blue/blue_ghost_up_1.png",
            "assets/ghost/blue/blue_ghost_up_2.png",
        ]
    }

    def new_target_cell(
        self,
        maze: list[list[int]],
        pos: tuple[int, int]
      ) -> list[Direction] | None:

        self.step = 0
        self.target_cell = None
        while not self.target_cell:
            y = random.randint(0, len(maze) - 1)
            x = random.randint(0, len(maze[0]) - 1)
            try:
                self.target_cell = solver_heap(
                    maze,
                    (pos[0], pos[1]),
                    (y, x),
                )
            except (ValueError, MisplaceCell):
                pass


class GhostRed(GhostLogic):
    ...
