import pygame

from menu import Menu
from monitor import Monitor
from enum_packman import Menu_name, Direction

pygame.init()
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

FRAME_RATE = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
MIN_W, MIN_H = 1280, 720

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

menu = Menu(screen, screen.get_size())

monitor = Monitor(screen)

running = True
while running:
    monitor.windows_resized = False
    monitor.key_press = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                monitor.menu = Menu_name.Menu.value
            elif event.key in {
                pygame.K_UP,
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_DOWN
            }:
                if event.key == pygame.K_UP:
                    monitor.key_press = Direction.up
                if event.key == pygame.K_LEFT:
                    monitor.key_press = Direction.left
                if event.key == pygame.K_RIGHT:
                    monitor.key_press = Direction.right
                if event.key == pygame.K_DOWN:
                    monitor.key_press = Direction.down

        elif event.type == pygame.VIDEORESIZE:
            monitor.windows_resized = True
            if event.w < MIN_W or event.h < MIN_H:
                screen = pygame.display.set_mode(
                    (
                        max(event.w, MIN_W),
                        max(event.h, MIN_H)
                    ), pygame.RESIZABLE)

    menu.display(monitor)
    pygame.display.update()

    clock.tick(FRAME_RATE)
