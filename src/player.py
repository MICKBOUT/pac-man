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

    def _reszie_img(self):
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
            player_pos: tuple[int, int],
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

    def __init__(self, start_pos: tuple[int, int], maze: list[list[int]]):
        self.pos = list(start_pos)
        self.direction = Direction.no_direction
        self.maze = maze
        self.buffer_direction = Direction.no_direction

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

    def update(self, key_press: Direction):

        if key_press:
            self.buffer_direction = key_press

        if self.buffer_direction.value and self.can_go(self.buffer_direction):
            self.direction = self.buffer_direction
            self.buffer_direction = Direction.no_direction

        if self.can_go(self.direction):
            match self.direction:
                case Direction.right:
                    self.pos[1] += self.SPEED
                case Direction.down:
                    self.pos[0] += self.SPEED
                case Direction.left:
                    self.pos[1] -= self.SPEED
                case Direction.up:
                    self.pos[0] -= self.SPEED
