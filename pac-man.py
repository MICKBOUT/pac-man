import pygame

import mazegenerator

pygame.init()
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

frame_rate = 60
screen_width = 1280
screen_high = 720

screen = pygame.display.set_mode((screen_width, screen_high))

center_x = (screen_width // 2)
center_y = (screen_high // 2)
running = True


# -North wall: Blocks movement to the cell above. Encoded with the bit 0.
# -East wall: Blocks movement to the cell on the right. Encoded with the bit 1.
# -South wall: Blocks movement to the cell below. Encoded with the bit 2.
# -West wall: Blocks movement to the cell on the left. Encoded with the bit 3.
def draw_maze(maze_grid: list[list[int]]):
    cell_size = 32

    center_x, center_y = screen_width // 2, screen_high // 2

    len_maze_x, len_maze_y = len(maze_grid[0]), len(maze_grid)
    offset_x = center_x - (len_maze_x * cell_size // 2)
    offset_y = center_y - (len_maze_y * cell_size // 2)

    for y, line in enumerate(maze_grid):
        for x, cell in enumerate(line):
            draw_cell(
                cell,
                offset_x + x * cell_size,
                offset_y + y * cell_size,
                cell_size
            )


def draw_cell(wall: int, offset_x: int, offset_y: int, cell_size: int):

    # North
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x, offset_y),
            (offset_x + cell_size, offset_y)
        )
    # East
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x + cell_size, offset_y),
            (offset_x + cell_size, offset_y + cell_size)
        )
    # South
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x, offset_y + cell_size),
            (offset_x + cell_size, offset_y + cell_size)
        )
    # West
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x, offset_y),
            (offset_x, offset_y + cell_size)
        )


maze_gen = mazegenerator.MazeGenerator((20, 20))
maze_grid = maze_gen.maze
while running:
    screen.fill((0, 0, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_maze(maze_grid)

    pygame.display.update()
    clock.tick(frame_rate)
