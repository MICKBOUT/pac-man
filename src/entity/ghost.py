import random
from abc import abstractmethod, ABC
from typing import Optional, TYPE_CHECKING

import pygame

# from monitor import Monitor
from entity.entity import EntityLogic, EntityDraw
from entity.solver import solver_heap
from enum_pacman import Direction
from entity.solver import MisplaceCell

if TYPE_CHECKING:
    from monitor import Monitor


class GhostLogic(EntityLogic, ABC):
    """Logic base class for ghost movement and state.

    Extends `EntityLogic` to add ghost-specific state such as pathing,
    vulnerability and return-home behavior.

    Attributes:
        target_path: Sequence of `Direction` steps the ghost will follow.
        target_cell: Optional grid cell that is the current high-level goal.
        step: Index into `target_path` for the next movement step.
        return_home: Flag indicating the ghost is returning to its start.
        pac_man_dead: Flag set when Pac-Man has been caught (unused here).
        vulnerable: Whether the ghost is vulnerable to being eaten.
        vulnerable_timer: Frames remaining while vulnerable.
    """

    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int]
    ) -> None:
        """Initialize ghost logic state.

        Args:
            maze: 2D maze grid used for pathfinding decisions.
            start_pos: Starting `(y, x)` cell to return to when eaten.
        """
        super().__init__(maze, start_pos)
        self.target_path: list[Direction] = []
        self.target_cell: Optional[tuple[int, int]] = None
        self.step: int = 0
        self.return_home = False
        self.pac_man_dead = False
        self.vulnerable: bool = False
        self.vulnerable_timer: int = 0
        self.new_target_cell()

    def set_vulnerable(self, duration_frames: int) -> None:
        """Mark the ghost as vulnerable for `duration_frames` frames.

        Args:
            duration_frames: Number of update frames the ghost remains
                vulnerable.
        """
        self.vulnerable = True
        self.vulnerable_timer = duration_frames

    @abstractmethod
    def new_target_cell(
           self,
           player_pos: tuple[int, int] = (0, 0)
         ) -> None:
        """Choose a new `target_cell` and compute a `target_path`.

        Implementations should populate `self.target_path` and optionally
        set `self.target_cell` to indicate the high-level goal cell.

        Args:
            player_pos: Current player `(y, x)` used by chasing ghosts.
        """
        pass

    def update(self, player_pos: tuple[int, int] = (0, 0)) -> None:
        """Advance ghost state by one tick, updating movement and timers.

        The method handles vulnerable timer decrementing, target path
        selection when necessary, and progression along `target_path`.

        Args:
            player_pos: Current player `(y, x)` position for target logic.
        """
        if self.vulnerable:
            self.vulnerable_timer -= 1
            if self.vulnerable_timer <= 0:
                self.vulnerable = False

        if not self.target:
            if self.step >= len(self.target_path):  # also set self.step to 0
                if self.return_home:
                    self.return_home = False
                self.new_target_cell(player_pos)
            self.direction = self.target_path[self.step]
            dir_y, dir_x = self.direction.value
            self.target = (self.pos[0] + dir_y, self.pos[1] + dir_x)

        if self.target:
            self.delta_movment += 1
            if self.delta_movment >= self.STEP_BY_CELL:
                self.pos = self.target
                self.target = None
                self.delta_movment = 0
                self.step += 1


class GhostDraw(GhostLogic, EntityDraw):
    """Rendering-capable ghost combining `GhostLogic` and `EntityDraw`.

    This class loads image assets for normal and vulnerable states and
    handles drawing, debug visualization (ESP), and vulnerable flashing.
    """

    COLOR = (255, 255, 255, 255)
    IMAGES_PATHS: dict[Direction, list[str]] = {}
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
        monitor: Monitor,
        cell_size: int = 15
      ) -> None:
        """Initialize drawables and connect logic state.

        Args:
            maze: The maze grid used for pathfinding/state.
            start_pos: Starting `(y, x)` grid cell for this ghost.
            monitor: The `Monitor` instance (used for debug drawing).
            cell_size: Pixel size for scaling loaded images.
        """
        self.monitor = monitor
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
        """Scale loaded images to the current `cell_size`.

        Populates `self.assets` and auxiliary lists used for vulnerable
        rendering.
        """
        size = (self.cell_size, self.cell_size)
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
        """Draw the ghost on `surface`, including vulnerable rendering.

        Args:
            surface: `pygame.Surface` to draw onto.
            cell_resized: Optional new cell size to re-scale assets.
        """
        if cell_resized:
            self.cell_size = cell_resized
            self._reszie_img()
        self.internal_frame_counter += 1

        true_y, true_x = self.get_true_pos(self.cell_size)

        if self.monitor.esp and self.target_cell and not self.vulnerable:
            target_y, target_x = self.target_cell
            target_y *= self.cell_size
            target_x *= self.cell_size
            pygame.draw.circle(
                surface,
                self.COLOR, (
                    target_x + self.cell_size//2,
                    target_y + self.cell_size//2
                ), self.cell_size // 5,
            )
            pygame.draw.line(
                surface,
                self.COLOR,
                (true_x + self.cell_size // 2, true_y + self.cell_size // 2),
                (target_x + self.cell_size//2, target_y + self.cell_size//2)
            )

        if self.return_home:
            surface.blit(
                self.assets_eyes[0], ((true_x, true_y), self.rect.size)
            )
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

    def _random_flee_target(self) -> None:
        """Pick a random reachable target and compute a path to it.

        Used when the ghost is vulnerable and needs to flee.
        """
        self.step = 0
        self.target_path = []
        self.target = None
        self.delta_movment = 0
        while not self.target_path:
            y = random.randint(0, len(self.maze) - 1)
            x = random.randint(0, len(self.maze[0]) - 1)
            try:
                self.target_path = solver_heap(
                    self.maze,
                    self.pos,
                    (y, x),
                )
            except (ValueError, MisplaceCell):
                pass

    def go_home(self) -> None:
        """Compute a path back to the ghost's `start_pos`.

        If pathfinding fails, selects a random flee target instead.
        """
        self.step = 0
        self.target_path = []
        self.target = None
        self.delta_movment = 0
        try:
            self.target_path = solver_heap(
                self.maze,
                self.pos,
                self.start_pos,
            )
            if not self.target_path:
                raise ValueError("path empty")
        except Exception:
            self._random_flee_target()
            return


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
    COLOR = (37, 150, 190, 200)

    def new_target_cell(
        self,
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:
        self.step = 0
        self.target_path = []

        if self.vulnerable:
            self._random_flee_target()
            return

        while not self.target_path:
            y = random.randint(0, len(self.maze) - 1)
            x = random.randint(0, len(self.maze[0]) - 1)
            try:
                self.target_path = solver_heap(
                    self.maze,
                    self.pos,
                    (y, x),
                )
                self.target_cell = (y, x)
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
    COLOR = (255, 183, 255, 200)

    def new_target_cell(
        self,
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:

        self.step = 0
        self.target_path = []

        if self.vulnerable:
            self._random_flee_target()
            return
        if self.pos == player_pos:
            self.target_path = [Direction.no_direction]
            return

        while not self.target_path:
            try:
                path = solver_heap(self.maze, self.pos, player_pos)
                if path:
                    self.target_path = [path[0]]
                    y_add, x_add = self.target_path[0].value
                    start_y, start_x = self.pos
                    self.target_cell = (start_y + y_add, start_x + x_add)
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
    COLOR = (254, 1, 0, 200)

    def new_target_cell(
        self,
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:

        self.step = 0
        self.target_path = []

        if self.vulnerable:
            self._random_flee_target()
            return
        if self.pos == player_pos:
            self.target_path = [Direction.no_direction]
            return

        while not self.target_path:
            try:
                self.target_path = solver_heap(self.maze, self.pos, player_pos)
                self.target_cell = player_pos
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
    COLOR = (252, 162, 43, 200)

    def new_target_cell(
        self,
        player_pos: tuple[int, int] = (0, 0)
      ) -> None:
        """Select a new target cell located along the maze border.

        The orange ghost patrols to a randomly chosen border cell (top,
        bottom, left or right). When it arrives it picks a new border
        destination and repeats the process. If vulnerable, it will pick
        a random flee target instead.
        """

        self.step = 0
        self.target_path = []

        if self.vulnerable:
            self._random_flee_target()
            return

        while not self.target_path:
            on_side = random.randint(0, 1)
            if on_side:  # == 1:
                y = random.randint(0, len(self.maze) - 1)
                x = random.choice([0, len(self.maze[0]) - 1])
            else:
                y = random.choice([0, len(self.maze) - 1])
                x = random.randint(0, len(self.maze[0]) - 1)
            try:
                self.target_path = solver_heap(
                    self.maze,
                    self.pos,
                    (y, x),
                )
                self.target_cell = (y, x)
            except (ValueError, MisplaceCell):
                pass
