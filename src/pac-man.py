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
    """Return whether the application is running as a bundled package.

    Returns:
        True when running from a frozen/bundled executable (e.g.
        PyInstaller) otherwise False.
    """
    return bool(getattr(sys, "frozen", False))


def _resource_directory() -> Path:
    """Return the directory containing runtime resources.

    When the application is packaged the resources are extracted to the
    PyInstaller temporary directory (accessible via `sys._MEIPASS`).
    Otherwise the repository layout is used (two levels above this file).

    Returns:
        A `pathlib.Path` pointing at the resolved resource directory.
    """
    if _is_packaged():
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parent.parent


def _configuration_path() -> Path | None:
    """Return the path to the configuration file requested by the user.

    Behavior:
    - If a single CLI argument is provided it is treated as the path to
      a JSON configuration file.
    - When running packaged with no CLI args, a `config.json` placed
      next to the executable is used.
    - Otherwise an error is printed and the function returns ``None``.

    Returns:
        A resolved `pathlib.Path` when a configuration file was found,
        otherwise ``None``.
    """
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
    """Resolve a high-score filename relative to the configuration file.

    Args:
        config_path: The resolved configuration file path.
        highscore_filename: The high-score filename from the config (may
            be absolute or relative).

    Returns:
        A string containing the absolute path to the high-score file.
    """
    highscore_path = Path(highscore_filename).expanduser()
    if highscore_path.is_absolute():
        return str(highscore_path)
    return str(config_path.parent / highscore_path)


def manage_player_movment(monitor: Monitor, key: int) -> None:
    """Map keyboard events to `Monitor.key_press` directions.

    This helper normalizes several possible key bindings (arrow keys and
    WASD) to the `Direction` enum used by the game logic.

    Args:
        monitor: The `Monitor` instance to update.
        key: The integer key code from a Pygame `KEYDOWN` event.
    """
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
    """Application entry point: parse config, initialize subsystems.

    The function locates and validates the configuration file, sets up
    the resource directory, initializes Pygame and creates the main
    `Menu` and `Monitor` objects. It runs the primary event loop until
    the user quits.

    The function handles common startup errors (missing file, JSON
    decode errors, validation errors and permission problems) by
    printing a message and returning early.
    """
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
    except PermissionError:
        print("Error: You don't have the permision to open this file")
        return
    except Exception as e:
        print("Error", e)

    config_data.highscore_filename = _configure_highscore_path(
        config_path,
        config_data.highscore_filename,
    )
    # change the working directory to allow relative import even in package
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
        monitor.windows_resized = False
        monitor.add_life = monitor.add_timer = False
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
        try:
            menu.display(monitor)
        except Exception as e:
            print("Error:", e)
            return
        clock.tick(FRAME_RATE)


if __name__ == "__main__":
    main()
