from typing import Optional

import pygame

from enum_packman import Direction
from entity import EntityLogic, EntityDraw


class PlayerDraw(EntityDraw):
    IMAGES_PATHS = [
        "assets/pac-mam/pac-mac_frame0.png",
        "assets/pac-mam/pac-mac_frame1.png",
        "assets/pac-mam/pac-mac_frame2.png",
        "assets/pac-mam/pac-mac_frame3.png",
    ]

    def __init__(self, player: PlayerLogic, cell_size: int = 15) -> None:
        super().__init__(player, cell_size)

        self.dict_entity_assets: dict[Direction, list[pygame.Surface]] = {}
        self._reszie_img()

        self.image: pygame.Surface = self.dict_entity_assets[
            Direction.right][0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))

    def _reszie_img(self) -> None:
        self.dict_entity_assets[Direction.right] = [
            pygame.transform.scale(
                image,
                (
                    int(self.cell_size * self.FILL_RATIO),
                    int(self.cell_size * self.FILL_RATIO)
                )
            )
            for image in self.images_loaded
        ]
        self.dict_entity_assets[Direction.up] = [
            pygame.transform.rotate(image, 90)
            for image in self.dict_entity_assets[Direction.right]
        ]
        self.dict_entity_assets[Direction.left] = [
            pygame.transform.rotate(image, 180)
            for image in self.dict_entity_assets[Direction.right]
        ]
        self.dict_entity_assets[Direction.down] = [
            pygame.transform.rotate(image, 270)
            for image in self.dict_entity_assets[Direction.right]
        ]

    def draw(
            self,
            surface: pygame.Surface,
            cell_resized: Optional[int] = None
          ) -> None:
        if cell_resized:
            self.cell_size = cell_resized
            self._reszie_img()

        true_y, true_x = self.entity.get_true_pos(self.cell_size)
        surface.blit(
            self.dict_entity_assets[self.entity.direction][
                (self.internal_counter // 5) % len(
                    self.dict_entity_assets[Direction.right]
                )
            ],
            (
                (true_x, true_y),
                self.rect.size
            ),
        )


class PlayerLogic(EntityLogic):
    STEP_BY_CELL = 10

    def __init__(self, maze: list[list[int]], start_pos: tuple[int, int], ):
        super().__init__(maze, start_pos)

        self.buffer_direction = Direction.no_direction

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
            if self.target is None and self.can_go(self.buffer_direction):
                self.direction = self.buffer_direction
                self.buffer_direction = Direction.no_direction
                dir_y, dir_x = self.direction.value
                self.target = [self.pos[0] + dir_y, self.pos[1] + dir_x]
                self.delta_movment = 0
            # if the player want to go back in the cell he was
            elif self.target is not None and self.is_opposite_direction(
              self.direction,
              self.buffer_direction
            ):  # reverse the direction of the player
                self.pos, self.target = self.target, self.pos
                self.delta_movment = self.STEP_BY_CELL - self.delta_movment
                self.direction = self.buffer_direction
                self.buffer_direction = Direction.no_direction

        if self.target is not None:
            self.delta_movment += 1
            if self.delta_movment >= self.STEP_BY_CELL:
                self.pos = self.target
                self.target = None
                self.delta_movment = 0
        else:
            if self.can_go(self.direction):
                dir_y, dir_x = self.direction.value
                self.target = [self.pos[0] + dir_y, self.pos[1] + dir_x]
                self.delta_movment = 0
