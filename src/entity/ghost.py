import random

import pygame

from entity.entity import EntityLogic, EntityDraw
from entity.solver import solver_heap


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


class GhostLogic(EntityLogic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_target_cell()

    def new_target_cell(self) -> None:
        self.target_cell = None
        self.step = 0
        while not self.target_cell:
            y = random.randint(0, len(self.maze) - 1)
            x = random.randint(0, len(self.maze[0]) - 1)
            while self.maze[y][x] == 15:
                y = random.randint(0, len(self.maze) - 1)
                x = random.randint(0, len(self.maze[0]) - 1)
            try:
                self.target_cell = solver_heap(self.maze, self.pos, (y, x))
            except Exception:
                pass

    def update(self) -> None:
        if self.target is None:
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
                if self.step >= len(self.target_cell):
                    self.new_target_cell()
