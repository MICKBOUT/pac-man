import json
import os
import sys
from pathlib import Path

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


def _is_packaged() -> bool:
    """Return whether the game is running from a bundled executable."""
    return bool(getattr(sys, "frozen", False))


def _resource_directory() -> Path:
    """Return the directory containing bundled resources or the repository."""
    if _is_packaged():
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parent.parent


def _configuration_path() -> Path | None:
    """Return the requested config file or the bundled default config file."""
    arguments = sys.argv[1:]
    if len(arguments) == 1:
        return Path(arguments[0]).expanduser().resolve()
    if not arguments and _is_packaged():
        return Path(sys.executable).resolve().parent / "config.json"
    print("Error: pass exactly one JSON configuration file as an argument")
    return None


def _configure_highscore_path(
    config_path: Path,
    highscore_filename: str,
) -> str:
    """Resolve relative highscore files next to their configuration file."""
    highscore_path = Path(highscore_filename).expanduser()
    if highscore_path.is_absolute():
        return str(highscore_path)
    return str(config_path.parent / highscore_path)


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
    config_path = _configuration_path()
    if config_path is None:
        return

    try:
        config_data = validation(str(config_path))
    except FileNotFoundError:
        print(f"Error: file '{config_path}' not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error: '{config_path}' is not valid JSON ({e})")
        return
    except ValidationError as e:
        print(f"Error: invalid config in '{config_path}':")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            print(f"  - {loc}: {err['msg']}")
        return

    config_data.highscore_filename = _configure_highscore_path(
        config_path,
        config_data.highscore_filename,
    )
    os.chdir(_resource_directory())

    pygame.init()
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    menu = Menu(screen, screen.get_size())
    try:
        monitor = Monitor(screen, config_data)
    except Exception as m:
        print(m)
        return

    running = True
    while running:
        monitor.windows_resized = monitor.add_life = monitor.add_timer = False
        monitor.key_press = None
        monitor.screen_size = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # to-do: change this if w/ the dict of pressed key
            elif event.type == pygame.KEYDOWN:
                manage_player_movment(monitor, event.key)
                if event.key == pygame.K_e and monitor.menu == Menu_name.Play:
                    monitor.esp = not monitor.esp
                if event.key == pygame.K_q:
                    monitor.add_life = True
                if event.key == pygame.K_t:
                    monitor.add_timer = True
                if event.key == pygame.K_ESCAPE:
                    # switch b/w pause / play in game or return to menu
                    if monitor.menu == Menu_name.Play:
                        monitor.menu = Menu_name.Game_pause
                    elif monitor.menu == Menu_name.Game_pause:
                        monitor.menu = Menu_name.Play
                    elif monitor.menu != Menu_name.Win:
                        monitor.score = 0
                        monitor.menu = Menu_name.Menu

                if monitor.menu == Menu_name.Register:
                    if event.key == pygame.K_BACKSPACE:
                        monitor.register_txt = monitor.register_txt[:-1]
                    elif (len(monitor.register_txt) < 10 and
                          (event.unicode.isalnum() or
                           event.key == pygame.K_SPACE)):
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
