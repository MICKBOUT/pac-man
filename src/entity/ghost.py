import random

import pygame

from entity.entity import EntityLogic, EntityDraw
from typing import Any
from entity.solver import solver_heap
from enum_packman import Direction
from entity.solver import MisplaceCell


class GhostDraw(EntityDraw):
    IMAGES_PATHS = [
        "assets/animation/blue_gost/1.png",
        "assets/animation/blue_gost/2.png"
    ]

    def __init__(self, ghost: GhostLogic, cell_size: int = 15) -> None:
        super().__init__(ghost, cell_size)

        self._reszie_img()

        self.image: pygame.Surface = self.entity_assets[0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))

    def _reszie_img(self) -> None:
        self.entity_assets = [
            pygame.transform.scale(
                image,
                (
                    int(self.cell_size * self.FILL_RATIO),
                    int(self.cell_size * self.FILL_RATIO)
                )
            )
            for image in self.images_loaded
        ]

    # for this to work i need a var that stock the end cell, not just the path
    # def draw(self, *args: Any, **kwargs: Any):
    #     super().draw(*args, **kwargs)
    #     if self.entity.target_cell:
    #         y, x = var_that_stock_the_end_cell
    #         pygame.draw.rect(
    #             args[1], "blue", (
    #                 (
    #                     y * self.cell_size,
    #                     x * self.cell_size
    #                 ),
    #                 (self.cell_size, self.cell_size)
    #             )
    #         )


class GhostLogic(EntityLogic):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)
        self.target_cell: list[Direction] | None = None
        self.step: int = 0
        self.target_cell_algo = kwargs["target_cell_algo"]
        self.new_target_cell()

    def new_target_cell(self) -> None:
        self.step = 0
        while not self.target_cell:
            y = random.randint(0, len(self.maze) - 1)
            x = random.randint(0, len(self.maze[0]) - 1)
            while self.maze[y][x] == 15:
                y = random.randint(0, len(self.maze) - 1)
                x = random.randint(0, len(self.maze[0]) - 1)
            try:
                self.target_cell = solver_heap(
                    self.maze,
                    tuple(self.pos),
                    (y, x)
                )
            except Exception:
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
                    self.new_target_cell()


def target_cell_blue_ghost(maze: list[list[int]], pos: tuple[int, int]
                           ) -> list[Direction] | None:
    while True:
        y = random.randint(0, len(maze) - 1)
        x = random.randint(0, len(maze[0]) - 1)
        try:
            return solver_heap(
                maze,
                (pos[0], pos[1]),
                (y, x),
            )
        except (ValueError, MisplaceCell):
            pass
