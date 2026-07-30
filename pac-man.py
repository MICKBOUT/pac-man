import pygame

import mazegenerator

pygame.init()
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

frame_rate = 60
screen_width = 1280
screen_high = 720

screen = pygame.display.set_mode((screen_width, screen_high))

center_x, center_y = screen_width // 2, screen_high // 2
running = True

screen_background_color = 119, 51, 68
maze_background_color = 11, 0, 20
cell_wall_color = 245, 233, 226

maze_gen = mazegenerator.MazeGenerator((20, 20))
maze_grid = maze_gen.maze
len_maze_x, len_maze_y = len(maze_grid[0]), len(maze_grid)
cell_size = min(
    (screen_high - 10) // len_maze_y,
    (screen_width - 10) // len_maze_x,
)
pos_first_cell = (
    center_x - (len_maze_x * cell_size // 2),
    center_y - (len_maze_y * cell_size // 2)
)


# -North wall: Blocks movement to the cell above. Encoded with the bit 0.
# -East wall: Blocks movement to the cell on the right. Encoded with the bit 1.
# -South wall: Blocks movement to the cell below. Encoded with the bit 2.
# -West wall: Blocks movement to the cell on the left. Encoded with the bit 3.
def draw_maze(maze_grid: list[list[int]]):

    start_x, start_y = pos_first_cell
    pygame.draw.rect(
        screen,
        maze_background_color,
        ((start_x, start_y), (len_maze_x * cell_size, len_maze_y * cell_size)),
    )
    for y, line in enumerate(maze_grid):
        for x, cell in enumerate(line):
            draw_cell(
                cell,
                start_x + x * cell_size,
                start_y + y * cell_size,
                cell_size
            )


def draw_cell(wall: int, offset_x: int, offset_y: int, cell_size: int):

    # North
    if wall % 2:
        pygame.draw.line(
            screen,
            cell_wall_color,
            (offset_x, offset_y),
            (offset_x + cell_size, offset_y)
        )
    # East
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            cell_wall_color,
            (offset_x + cell_size, offset_y),
            (offset_x + cell_size, offset_y + cell_size)
        )
    # South
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            cell_wall_color,
            (offset_x, offset_y + cell_size),
            (offset_x + cell_size, offset_y + cell_size)
        )
    # West
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            cell_wall_color,
            (offset_x, offset_y),
            (offset_x, offset_y + cell_size)
        )


# to-do: put this in Player cls but idk why it dosn't work when i try it...
fill_ratio = 0.8


class Player(pygame.sprite.Sprite):
    image_loaded = [
        pygame.image.load("assets/pac-mam/pac-mac_frame0.png").convert_alpha(),
        pygame.image.load("assets/pac-mam/pac-mac_frame1.png").convert_alpha(),
        pygame.image.load("assets/pac-mam/pac-mac_frame2.png").convert_alpha(),
        pygame.image.load("assets/pac-mam/pac-mac_frame3.png").convert_alpha(),
    ]
    player_assets = [
        pygame.transform.scale(
            x,
            (int(cell_size * fill_ratio), int(cell_size * fill_ratio))
        )
        for x in image_loaded
    ]

    def __init__(self):
        self.image = self.player_assets[0]

        pos_start_x, pos_start_y = pos_first_cell
        pos_start_x += cell_size // 2
        pos_start_y += cell_size // 2

        self.rect = self.image.get_rect(center=(pos_start_x, pos_start_y))
        self.internal_counter = 0

    def draw(self):
        screen.blit(
            self.player_assets[
                (self.internal_counter // 5) % len(self.player_assets)
            ],
            self.rect
        )

    def update(self):
        self.internal_counter += 1


pac_mac = Player()

while running:
    screen.fill((119, 51, 68))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # update
    pac_mac.update()

    # draw
    draw_maze(maze_grid)
    pac_mac.draw()

    pygame.display.update()
    clock.tick(frame_rate)
