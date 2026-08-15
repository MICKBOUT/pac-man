import random
from abc import abstractmethod, ABC
from typing import Optional

import pygame

from entity.entity import EntityLogic, EntityDraw
from entity.solver import solver_heap
from enum_packman import Direction
from entity.solver import MisplaceCell


class GhostLogic(EntityLogic, ABC):
    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int]
    ) -> None:
        super().__init__(maze, start_pos)
        self.target_cell: Optional[list[Direction]] = None
        self.step: int = 0
        self.return_home = False
        self.vulnerable: bool = False
        self.vulnerable_timer: int = 0
        self.new_target_cell(maze, self.pos)

    def set_vulnerable(self, duration_frames: int) -> None:
        self.vulnerable = True
        self.vulnerable_timer = duration_frames
        if not self.return_home:
            self.target_cell = []
            self.target = []
            self.step = 0
        self.new_target_cell(self.maze, self.pos)

    @abstractmethod
    def new_target_cell(
           self,
           maze: list[list[int]],
           pos: tuple[int, int],
           player_pos: tuple[int, int] = (0, 0)
         ) -> None:
        pass

    def update(self, player_pos: Optional[tuple[int, int]] = (0, 0)) -> None:
        if self.vulnerable:
            self.vulnerable_timer -= 1
            if self.vulnerable_timer <= 0:
                self.vulnerable = False
                if not self.return_home:
                    self.target_cell = []
                    self.step = 0

        if not self.target:
            assert self.target_cell is not None
            self.direction = self.target_cell[self.step]
            dir_y, dir_x = self.direction.value
            self.target = [self.pos[0] + dir_y, self.pos[1] + dir_x]
            self.delta_movment = 0

        if self.target:
            self.delta_movment += 1
            if self.delta_movment >= self.STEP_BY_CELL:
                self.pos = self.target
                self.target = []
                self.delta_movment = 0
                self.step += 1
                assert self.target_cell is not None
                if self.step >= len(self.target_cell):
                    self.new_target_cell(self.maze, self.pos, player_pos)


class GhostDraw(GhostLogic, EntityDraw):
    VULNERABLE_IMAGES_PATHS = [
        "assets/ghost/vulnerable/vulnerable_1.png",
        "assets/ghost/vulnerable/vulnerable_2.png",
    ]
    VULNERABLE_FLASH_IMAGES_PATHS = [
      "assets/ghost/vulnerable/vulnerable_flash_1.png",
      "assets/ghost/vulnerable/vulnerable_flash_2.png",
    ]
    VULNERABLE_EYES = [
        "assets/ghost/vulnerable/eyes.png"
    ]
    VULNERABLE_FLASH_START = 60

    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int],
        cell_size: int = 15
      ) -> None:
        self.images_loaded = {
            key: [pygame.image.load(path).convert_alpha() for path in value]
            for key, value in self.IMAGES_PATHS.items()
        }
        self.images_loaded_vulnerable = [
            pygame.image.load(path).convert_alpha()
            for path in self.VULNERABLE_IMAGES_PATHS
        ]
        self.images_loaded_vulnerable_flash = [
            pygame.image.load(path).convert_alpha()
            for path in self.VULNERABLE_FLASH_IMAGES_PATHS
        ]
        self.images_loaded_eyes = [
            pygame.image.load(path).convert_alpha()
            for path in self.VULNERABLE_EYES
        ]
        EntityDraw.__init__(self, cell_size)
        GhostLogic.__init__(self, maze, start_pos)

    def _reszie_img(self) -> None:
        size = (
            int(self.cell_size * self.FILL_RATIO),
            int(self.cell_size * self.FILL_RATIO)
        )
        self.assets = {
            key: [pygame.transform.scale(image, size) for image in value]
            for key, value in self.images_loaded.items()
        }
        self.assets_vulnerable = [
            pygame.transform.scale(image, size)
            for image in self.images_loaded_vulnerable
        ]
        self.assets_vulnerable_flash = [
            pygame.transform.scale(image, size)
            for image in self.images_loaded_vulnerable_flash
        ]
        self.assets_eyes = [
            pygame.transform.scale(image, size)
            for image in self.images_loaded_eyes
        ]

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

        if self.return_home:
            surface.blit(self.assets_eyes[0],
                         ((true_x, true_y), self.rect.size))
            return

        if self.vulnerable:
            frames = (
                self.assets_vulnerable_flash
                if self.vulnerable_timer < self.VULNERABLE_FLASH_START
                else self.assets_vulnerable
            )
            image = frames[(self.internal_frame_counter // 5) % len(frames)]
            surface.blit(image, ((true_x, true_y), self.rect.size))
            return
        try:
            surface.blit(
                self.assets[self.direction][
                    (self.internal_frame_counter // 5) % self.nb_frame
                ],
                ((true_x, true_y), self.rect.size),
            )
        except KeyError:
            pass

    def _random_flee_target(self,
                            maze,
                            pos,
                            max_attempts: int = 50) -> list[Direction]:
        target_cell = None
        attempts = 0
        while not target_cell and attempts < max_attempts:
            attempts += 1
            y = random.randint(0, len(maze) - 1)
            x = random.randint(0, len(maze[0]) - 1)
            try:
                target_cell = solver_heap(maze, (pos[0], pos[1]), (y, x))
            except (ValueError, MisplaceCell):
                pass
        if not target_cell:
            target_cell = [Direction.no_direction]
        return target_cell

    def go_home(self, maze):
        if not self.return_home:
            try:
                sx, sy = self.start_pos
                start = self.pos
                path = solver_heap(maze, start, (sx, sy))
                if not path:
                    self.return_home = True
                    return
                self.step = 0
                self.target_cell = path
                self.target = []
                self.delta_movment = 0
                self.return_home = True
            except (ValueError, MisplaceCell):
                self.return_home = True


class GhostBlue(GhostDraw):
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
        pos: tuple[int, int],
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:
        self.step = 0
        self.target_cell = None

        if self.vulnerable:
            self.target_cell = self._random_flee_target(maze, pos)
            return
        while not self.target_cell:
            self.return_home = False
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


class GhostPink(GhostDraw):
    IMAGES_PATHS = {
        Direction.right: [
            "assets/ghost/pink/pink_ghost_right_1.png",
            "assets/ghost/pink/pink_ghost_right_2.png"
        ],
        Direction.down: [
            "assets/ghost/pink/pink_ghost_down_1.png",
            "assets/ghost/pink/pink_ghost_down_2.png",
        ],
        Direction.left: [
            "assets/ghost/pink/pink_ghost_left_1.png",
            "assets/ghost/pink/pink_ghost_left_2.png",
        ],
        Direction.up: [
            "assets/ghost/pink/pink_ghost_up_1.png",
            "assets/ghost/pink/pink_ghost_up_2.png",
        ]
    }

    def new_target_cell(
        self,
        maze: list[list[int]],
        pos: tuple[int, int],
        player_pos: tuple[int, int] = (0, 0)
    ) -> None:

        self.step = 0
        self.target_cell = None

        if self.vulnerable:
            self.target_cell = self._random_flee_target(maze, pos)
            return
        while not self.target_cell:
            self.return_home = False
            y, x = player_pos
            if (pos[0], pos[1]) == (y, x):
                self.target_cell = [Direction.no_direction]
                break
            try:
                path = solver_heap(maze, (pos[0], pos[1]), (y, x))
                if path:
                    self.target_cell = [path[0]]
            except (ValueError, MisplaceCell):
                pass


class GhostRed(GhostDraw):
    IMAGES_PATHS = {
        Direction.right: [
            "assets/ghost/red/red_ghost_right_1.png",
            "assets/ghost/red/red_ghost_right_2.png"
        ],
        Direction.down: [
            "assets/ghost/red/red_ghost_down_1.png",
            "assets/ghost/red/red_ghost_down_2.png",
        ],
        Direction.left: [
            "assets/ghost/red/red_ghost_left_1.png",
            "assets/ghost/red/red_ghost_left_2.png",
        ],
        Direction.up: [
            "assets/ghost/red/red_ghost_up_1.png",
            "assets/ghost/red/red_ghost_up_2.png",
        ]
    }

    def new_target_cell(
        self,
        maze: list[list[int]],
        pos: tuple[int, int],
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:

        self.step = 0
        self.target_cell = None

        if self.vulnerable:
            self.target_cell = self._random_flee_target(maze, pos)
            return
        while not self.target_cell:
            self.return_home = False
            y, x = player_pos
            if (pos[0], pos[1]) == (y, x):
                self.target_cell = [Direction.no_direction]
                break
            try:
                path = solver_heap(maze, (pos[0], pos[1]), (y, x))
                if path:
                    self.target_cell = path
            except (ValueError, MisplaceCell):
                pass


class GhostOrange(GhostDraw):
    IMAGES_PATHS = {
        Direction.right: [
            "assets/ghost/orange/orange_ghost_right_1.png",
            "assets/ghost/orange/orange_ghost_right_2.png"
        ],
        Direction.down: [
            "assets/ghost/orange/orange_ghost_down_1.png",
            "assets/ghost/orange/orange_ghost_down_2.png",
        ],
        Direction.left: [
            "assets/ghost/orange/orange_ghost_left_1.png",
            "assets/ghost/orange/orange_ghost_left_2.png",
        ],
        Direction.up: [
            "assets/ghost/orange/orange_ghost_up_1.png",
            "assets/ghost/orange/orange_ghost_up_2.png",
        ]
    }

    def new_target_cell(
        self,
        maze: list[list[int]],
        pos: tuple[int, int],
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:
        """
        This ghost goes on a wall, either on the left, right, bottom, or top of
        the maze, once the ghost arrive at its destination, it repeats this
        procces.
        """

        self.step = 0
        self.target_cell = None

        if self.vulnerable:
            self.target_cell = self._random_flee_target(maze, pos)
            return
        while not self.target_cell:
            self.return_home = False
            on_side = random.randint(0, 1)
            if on_side:  # == 1:
                y = random.randint(0, len(maze) - 1)
                x = random.choice([0, len(maze[0]) - 1])
            else:
                y = random.choice([0, len(maze) - 1])
                x = random.randint(0, len(maze[0]) - 1)
            try:
                self.target_cell = solver_heap(
                    maze,
                    (pos[0], pos[1]),
                    (y, x),
                )
            except (ValueError, MisplaceCell):
                pass
