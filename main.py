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
offset = [0, 0]

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(frame_rate)


def main():
    print("Hello from pac-mac!")

    # min 14 by 10
    maze_gen = mazegenerator.MazeGenerator((14, 10))
    maze_gen


if __name__ == "__main__":
    main()








