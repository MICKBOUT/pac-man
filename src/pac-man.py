import json
import sys

import pygame
from pydantic import ValidationError

from menu import Menu
from monitor import Monitor
from enum_pacman import Menu_name, Direction
from validation.validate import validation

FRAME_RATE = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
MIN_W = 1280
MIN_H = 720
SET_MOVMENT_KEY = {
    pygame.K_UP, pygame.K_w,
    pygame.K_LEFT, pygame.K_a,
    pygame.K_RIGHT, pygame.K_d,
    pygame.K_DOWN, pygame.K_s,
}


def manage_player_movment(monitor: Monitor, key: int) -> None:
    if key in SET_MOVMENT_KEY:
        if key in {pygame.K_UP, pygame.K_w}:
            monitor.key_press = Direction.up
        if key in {pygame.K_LEFT, pygame.K_a}:
            monitor.key_press = Direction.left
        if key in {pygame.K_RIGHT, pygame.K_d}:
            monitor.key_press = Direction.right
        if key in {pygame.K_DOWN, pygame.K_s}:
            monitor.key_press = Direction.down


def main() -> None:
    try:
        filename = sys.argv[1]
    except Exception:
        print("Error: please, pass the config file as parametor")
        return

    try:
        config_data = validation(filename)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error: '{filename}' is not valid JSON ({e})")
        return
    except ValidationError as e:
        print(f"Error: invalid config in '{filename}':")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            print(f"  - {loc}: {err['msg']}")
        return

    pygame.init()
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    menu = Menu(screen, screen.get_size())
    monitor = Monitor(screen, config_data)

    running = True
    while running:
        monitor.windows_resized = False
        monitor.key_press = None
        monitor.screen_size = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # to-do: change this if w/ the dict of pressed key
            elif event.type == pygame.KEYDOWN:
                manage_player_movment(monitor, event.key)
                if event.key == pygame.K_e:
                    monitor.esp = not monitor.esp
                if event.key == pygame.K_ESCAPE:
                    # switch b/w pause / play in game or return to menu
                    if monitor.menu == Menu_name.Play:
                        monitor.menu = Menu_name.Game_pause
                    elif monitor.menu == Menu_name.Game_pause:
                        monitor.menu = Menu_name.Play
                    else:
                        monitor.menu = Menu_name.Menu

                if monitor.menu == Menu_name.Register:
                    if event.key == pygame.K_BACKSPACE:
                        monitor.register_txt = monitor.register_txt[:-1]
                    elif (len(monitor.register_txt) < 10 and
                          event.unicode.isalpha()):
                        monitor.register_txt += event.unicode

            elif event.type == pygame.VIDEORESIZE:
                monitor.windows_resized = True
                if event.w < MIN_W or event.h < MIN_H:
                    screen = pygame.display.set_mode((
                            max(event.w, MIN_W),
                            max(event.h, MIN_H)
                        ), pygame.RESIZABLE
                    )

        pygame.display.update()
        menu.display(monitor)
        clock.tick(FRAME_RATE)


if __name__ == "__main__":
    main()
