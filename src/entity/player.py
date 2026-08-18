from typing import Optional

import pygame

from enum_pacman import Direction
from entity.entity import EntityLogic, EntityDraw


class PlayerLogic(EntityLogic):
    STEP_BY_CELL = 10

    def __init__(self,
                 maze: list[list[int]],
                 start_pos: tuple[int, int],
                 monitor):
        super().__init__(maze, start_pos)
        self.buffer_direction = Direction.no_direction
        self.life = monitor.config_data.lives
        self.dead = False

    @staticmethod
    def is_opposite_direction(
        first_dir: Direction,
        seconde_dir: Direction
    ) -> bool:
        if (
                first_dir == Direction.no_direction or
                seconde_dir == Direction.no_direction
        ):  # early exit if one direction is Null
            return False

        if first_dir == Direction.up and seconde_dir == Direction.down:
            return True
        elif first_dir == Direction.down and seconde_dir == Direction.up:
            return True
        elif first_dir == Direction.left and seconde_dir == Direction.right:
            return True
        elif first_dir == Direction.right and seconde_dir == Direction.left:
            return True
        return False

    def update(self, key_press: Optional[Direction] = None) -> None:

        if key_press:
            self.buffer_direction = key_press

        # try to go in the direction of the buffer
        if self.buffer_direction:
            # if the player is exactry on the cell
            if (not self.target) and self.can_go(self.buffer_direction):
                self.direction = self.buffer_direction
                self.buffer_direction = Direction.no_direction
                dir_y, dir_x = self.direction.value
                self.target = (self.pos[0] + dir_y, self.pos[1] + dir_x)
                self.delta_movment = 0
            # if the player want to go back in the cell he was
            elif self.target and self.is_opposite_direction(
              self.direction,
              self.buffer_direction
            ):  # reverse the direction of the player
                self.pos, self.target = self.target, self.pos
                self.delta_movment = self.STEP_BY_CELL - self.delta_movment
                self.direction = self.buffer_direction
                self.buffer_direction = Direction.no_direction

        if self.target:
            self.delta_movment += 1
            if self.delta_movment >= self.STEP_BY_CELL:
                self.pos = self.target
                self.target = None
                self.delta_movment = 0
        else:
            if self.can_go(self.direction):
                dir_y, dir_x = self.direction.value
                self.target = (self.pos[0] + dir_y, self.pos[1] + dir_x)
                self.delta_movment = 0


class PlayerDraw(PlayerLogic, EntityDraw):
    IMAGES_PATHS = [
        "assets/pac-mam/pac-mac_frame0.png",
        "assets/pac-mam/pac-mac_frame1.png",
        "assets/pac-mam/pac-mac_frame2.png",
        "assets/pac-mam/pac-mac_frame3.png",
    ]

    def __init__(
        self,
        maze: list[list[int]], start_pos: tuple[int, int],
        monitor,
        cell_size: int = 15
      ) -> None:
        self.images_loaded = [
            pygame.image.load(path).convert_alpha()
            for path in self.IMAGES_PATHS
        ]
        EntityDraw.__init__(self, cell_size)
        PlayerLogic.__init__(self, maze, start_pos, monitor)

    def _reszie_img(self) -> None:
        self.assets[Direction.right] = [
            pygame.transform.scale(
                image, (
                    int(self.cell_size * self.FILL_RATIO),
                    int(self.cell_size * self.FILL_RATIO)
                )
            )
            for image in self.images_loaded
        ]
        self.assets[Direction.up] = [
            pygame.transform.rotate(image, 90)
            for image in self.assets[Direction.right]
        ]
        self.assets[Direction.left] = [
            pygame.transform.rotate(image, 180)
            for image in self.assets[Direction.right]
        ]
        self.assets[Direction.down] = [
            pygame.transform.rotate(image, 270)
            for image in self.assets[Direction.right]
        ]
