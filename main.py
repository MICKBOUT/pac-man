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
def draw_cell(wall: int, offset_x: int, offset_y):
    cell_size = 32

    # North
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x * cell_size, offset_y * cell_size),
            ((offset_x + 1) * cell_size, offset_y * cell_size)
        )
    # East
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            ((offset_x + 1) * cell_size, offset_y * cell_size),
            ((offset_x + 1) * cell_size, (offset_y + 1) * cell_size)
        )
    # South
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x * cell_size, (offset_y + 1) * cell_size),
            ((offset_x + 1) * cell_size, (offset_y + 1) * cell_size)
        )
    # West
    wall //= 2
    if wall % 2:
        pygame.draw.line(
            screen,
            "red",
            (offset_x * cell_size, offset_y * cell_size),
            (offset_x * cell_size, (offset_y + 1) * cell_size)
        )


maze_gen = mazegenerator.MazeGenerator((20, 20))
maze_grid = maze_gen.maze
while running:
    screen.fill((0, 0, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for y, line in enumerate(maze_grid):
        for x, cell in enumerate(line):
            draw_cell(cell, x, y)

    pygame.display.update()
    clock.tick(frame_rate)
