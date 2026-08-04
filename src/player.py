from typing import Optional

import pygame

from enum_packman import Direction


class PlayerDraw(pygame.sprite.Sprite):
    FILL_RATIO = 1

    def __init__(self, cell_size: int = 15) -> None:
        self.image_loaded = [
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame0.png").convert_alpha(),
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame1.png").convert_alpha(),
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame2.png").convert_alpha(),
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame3.png").convert_alpha(),
        ]
        self.player_assets = [
                pygame.transform.scale(
                        x,
                        (
                            int(cell_size * self.FILL_RATIO),
                            int(cell_size * self.FILL_RATIO)
                        )
                )
                for x in self.image_loaded
            ]
        self.image: pygame.Surface = self.player_assets[0]

        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))
        self.internal_counter = 0

    def _reszie_img(self) -> None:
        self.player_assets = [
                pygame.transform.scale(
                        x,
                        (
                            int(self.cell_size * self.FILL_RATIO),
                            int(self.cell_size * self.FILL_RATIO)
                        )
                )
                for x in self.image_loaded
            ]

    def update(self) -> None:
        self.internal_counter += 1

    def draw(
            self,
            surface: pygame.Surface,
            player_pos: list[int],
            cell_resized: Optional[int] = None
          ) -> None:
        # rescale the image if the window has change size
        if cell_resized:
            self.cell_size = cell_resized
            self._reszie_img()

        y, x = player_pos
        true_y, true_x = y * self.cell_size, x * self.cell_size
        # draw the player on the screen
        surface.blit(
            self.player_assets[
                (self.internal_counter // 5) % len(self.player_assets)
            ],
            (
                (true_x, true_y),
                self.rect.size
            ),
        )


class PlayerLogic():
    SPEED = 1
    STEP_BY_CELL = 10

    def __init__(self, start_pos: tuple[int, int], maze: list[list[int]]):
        self.maze = maze
        self.pos = list(start_pos)
        self.current_cell = self.pos

        self.direction = Direction.no_direction
        self.buffer_direction = Direction.no_direction
        self.target: Optional[list[int]] = None
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
                self.pos, self.target = self.pos, self.target
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
