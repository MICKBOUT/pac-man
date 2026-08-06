import random

import pygame

from enum_packman import Direction
from entity import EntityLogic, EntityDraw


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
