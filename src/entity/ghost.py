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
        self.new_target_cell(maze, self.pos)

    @abstractmethod
    def new_target_cell(
        self,
        maze: list[list[int]],
        pos: tuple[int, int],
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:
        pass

    def update(self, player_pos: Optional[tuple[int, int]] = (0, 0)) -> None:
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
    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int],
        cell_size: int = 15
      ) -> None:
        self.images_loaded = {
            key: [
                pygame.image.load(path).convert_alpha()
                for path in value
            ]
            for key, value in self.IMAGES_PATHS.items()
        }
        EntityDraw.__init__(self, cell_size)
        GhostLogic.__init__(self, maze, start_pos)

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

    def go_home(self, pac_man_pos, maze):
        try:
            self.target_cell = solver_heap(maze, pac_man_pos, self.start_pos)
        except (ValueError, MisplaceCell):
            pass


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
        while not self.target_cell:
            y, x = player_pos
            try:
                self.target_cell = [solver_heap(
                    maze,
                    (pos[0], pos[1]),
                    (y, x),
                )[0]]
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
        while not self.target_cell:
            y, x = player_pos
            try:
                self.target_cell = solver_heap(
                    maze,
                    (pos[0], pos[1]),
                    (y, x),
                )
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
        while not self.target_cell:
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
