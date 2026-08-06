import pygame

from enum_packman import Direction


class EntityDraw():
    FILL_RATIO = 1
    IMAGES_PATHS = []

    def __init__(self, entity, cell_size):
        self.entity = entity
        self.cell_size = cell_size

        self.images_loaded = [
            pygame.image.load(path).convert_alpha()
            for path in self.IMAGES_PATHS
        ]

        self.internal_counter = 0

    def update(self) -> None:
        self.internal_counter += 1

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
            self.entity_assets[self.entity.direction][
                (self.internal_counter // 5) % len(
                    self.entity_assets[Direction.right]
                )
            ],
            (
                (true_x, true_y),
                self.rect.size
            ),
        )


class EntityLogic:
    STEP_BY_CELL = 13

    def __init__(
        self,
        maze: list[list[int]],
        start_pos: tuple[int, int] = (0, 0)
      ) -> None:
        self.pos = list(start_pos)
        self.maze = maze
        self.direction = Direction.right
        self.target = None

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

    def get_true_pos(self, cell_size: int) -> tuple[int, int]:
        y, x = map(lambda x: x * cell_size, self.pos)
        if self.target is None:
            return y, x

        offset = (cell_size / self.STEP_BY_CELL) * self.delta_movment
        offset_y, offset_x = map(lambda x: x*offset, self.direction.value)

        return y + offset_y, x + offset_x
