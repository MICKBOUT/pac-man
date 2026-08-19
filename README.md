*This project has been created as part of the 42 curriculum by mboutte, mbichet.*

# Pac-Man

## Description

Pac-Man is a graphical Python recreation of the arcade game. Guide Pac-Man through generated mazes, collect Pac-Gums, avoid the four ghosts, and use Super Pac-Gums to make the ghosts vulnerable. The game includes a menu, pause screen, rules screen, score entry, and a persistent top-ten highscore table.

The game is built with Pygame CE and uses the assigned `mazegenerator` package to create its mazes. A game ends when the player runs out of lives, the level timer expires, or the required levels are completed.

## Instructions

### Requirements

- Python 3.14 or later (the version declared by this repository)
- [uv](https://docs.astral.sh/uv/), used to create the environment and install dependencies
- A graphical desktop session capable of running Pygame

### Install and run

From the repository root:

```sh
uv sync
uv run src/pac-man.py config.json
```

The same game command is available through:

```sh
make run
```

The program takes one JSON configuration file argument. For example:

```sh
uv run src/pac-man.py path/to/my-config.json
```

If the configuration file is missing, malformed, or contains an invalid value, the launcher displays a readable error message rather than a Python traceback.

### Controls

| Input | Action |
| --- | --- |
| Arrow keys or `W` / `A` / `S` / `D` | Move Pac-Man |
| `Esc` | Pause or resume a game; return to the menu from a non-game screen |
| `E` | Toggle the ghost-target debug overlay |
| `Q` | Add an extra life (review/debug aid) |
| `T` | Add time (review/debug aid) |
| Mouse | Use menu, pause, score, and name-registration buttons |
| Backspace | Delete a character while entering a highscore name |

During score registration, names are limited to 10 characters and may contain letters, numbers, and spaces.

## Configuration

Pass the configuration file as the sole command-line argument. The current loader reads standard JSON; use the provided [config.json](config.json) as a starting point.

```json
{
  "highscore_filename": "scores.json",
  "level": [1],
  "width": 16,
  "height": 10,
  "lives": 3,
  "pacgum": 60,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90
}
```

| Key | Meaning | Default / constraint |
| --- | --- | --- |
| `highscore_filename` | JSON file used to store scores | Required |
| `level` | List of seeds used before random levels are generated | Required; `[1]` in the supplied configuration |
| `width`, `height` | Maze dimensions in cells | `16`, `10`; minimum `14`, `10` |
| `lives` | Lives at the start of a game | `3`; minimum `1` |
| `pacgum` | Number of regular Pac-Gums placed in a maze | `60` |
| `points_per_pacgum` | Points for a regular Pac-Gum | `10`; non-negative |
| `points_per_super_pacgum` | Points for a Super Pac-Gum | `50`; non-negative |
| `points_per_ghost` | Points for an edible ghost | `200`; non-negative |
| `seed` | Seed for the first maze | `42`; non-negative |
| `level_max_time` | Time limit for each level, in seconds | `90`; minimum `1` |

Unknown keys are ignored by the configuration model. The first maze is generated from `seed`; later levels use the configured seed list and then generated mazes. The game completes after at least ten levels.

## Gameplay

- Pac-Man begins in the maze centre with the configured number of lives.
- Four ghosts begin in the maze corners. They navigate corridors autonomously; some pursue Pac-Man while others choose a random destination.
- A normal Pac-Gum awards `points_per_pacgum` points. Four Super Pac-Gums are placed in the maze corners and award `points_per_super_pacgum` points.
- A Super Pac-Gum makes ghosts vulnerable temporarily. Eating one awards `points_per_ghost`; it returns home before rejoining the maze.
- Clearing every Pac-Gum moves the game to the next level while preserving score and remaining lives.
- Press `Esc` while playing to open the pause menu. It can resume the game or abandon it and return to the main menu.

### Debug / cheat aid

Pressing `E` toggles a visual overlay that displays each non-vulnerable ghost’s next target and direction. `Q` adds a life and `T` adds time. These controls are intended to make ghost movement and gameplay easier to inspect during evaluation.


## Highscore system

Highscores are stored persistently as JSON in the file specified by `highscore_filename` (by default, [scores.json](scores.json)). Each entry contains a player `name` and non-negative integer `score`.

At startup, the score file is loaded for the highscore screen. Missing or unreadable files are recreated as empty score data. After a win or game over, a score that qualifies for the table prompts the player for a name. Entries are sorted in descending score order and only the ten best are retained.

JSON was chosen because it is human-readable, portable, and sufficient for a small local leaderboard without a database or network service.

## Maze generation

[custom_maze.py](src/custom_maze.py) adapts the assigned external `mazegenerator` package rather than implementing a maze generator in this project. `Maze` subclasses `mazegenerator.MazeGenerator`, passes the selected dimensions and seed to it, then uses the returned wall data to draw the maze in Pygame. The rest of the game only depends on the resulting grid, which keeps generation separate from drawing and gameplay logic.

## Implementation

The application runs a 60 FPS Pygame event loop in [pac-man.py](src/pac-man.py). It validates the configuration, creates a shared `Monitor` state object, dispatches input, and asks the menu or current game to draw each frame.

`Game` owns the maze, player, ghosts, Pac-Gums, timer, and gameplay update cycle. Collision helpers apply scoring, remove consumed Pac-Gums, set ghost vulnerability, and manage player deaths. The ghost implementations use the heap-based solver to choose paths through maze corridors. Pygame surfaces and sprites are kept in the drawing classes, while movement and path state remain in logic classes.

## General Software Architecture

```text
pac-man.py
  ├── validation/validate.py      configuration → ConfigModel
  ├── Monitor                    shared game state
  └── Menu                       screen-state dispatcher
        ├── Game
        │     ├── Maze (custom_maze.py → mazegenerator)
        │     ├── PlayerDraw / PlayerLogic
        │     ├── Ghost*Draw / GhostLogic → solver_heap
        │     ├── PacGum
        │     └── collision helpers
        └── register.py           JSON highscore load/save
```

The UI is divided into menu screens (`menu.py`, `button.py`, `texte_zone.py`) and game drawing. The `entity/` package groups the reusable movement, player, ghost, collision, and pathfinding components. Static sprites and scene art are kept under `assets/`.

## Project Management

Project-management material and team evidence belong in the dedicated [project_management](project_management/) directory. The project was developed iteratively: the team first established the playable maze, movement, and collision loop, then added ghosts, scoring, menus, persistent scores, and validation. Changes were integrated through Git commits and merge commits; remaining verification and delivery evidence can be recorded alongside the project-management documents.

## Resources

- [Pygame CE documentation](https://pyga.me/docs/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [Python `json` module documentation](https://docs.python.org/3/library/json.html)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [Pac-Man history, The Strong National Museum of Play](https://www.museumofplay.org/games/pac-man/)
- [uv documentation](https://docs.astral.sh/uv/)

### AI use

An AI assistant was used to review the assignment’s README requirements, inspect the existing codebase, and prepare the initial documentation draft. The team must review this document, verify every statement against the implementation, and remain responsible for the final content.
