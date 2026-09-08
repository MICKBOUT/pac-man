import json

from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    """Pydantic model describing valid configuration fields.

    Attributes:
        highscore_filename: Path or filename used to persist highscores.
        level: List of integers describing the level layout identifier(s).
        width: Maze width in cells (between 14 and 40).
        height: Maze height in cells (between 10 and 40).
        lives: Number of player lives (>= 1).
        pacgum: Total number of pac-gums to place on the map.
        points_per_pacgum: Points awarded for a regular pac-gum (>= 0).
        points_per_super_pacgum: Points for a super pac-gum (>= 0).
        points_per_ghost: Points awarded when eating a vulnerable ghost (>= 0).
        seed: RNG seed used for deterministic placement (>= 0).
        level_max_time: Maximum time for the level in seconds (>= 1).
    """
    highscore_filename: str
    level: list[int]
    width: int = Field(ge=14, le=40)
    height: int = Field(ge=10, le=40)
    lives: int = Field(ge=1)
    pacgum: int
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    seed: int = Field(ge=0)
    level_max_time: int = Field(ge=1)


def validation(filename: str) -> ConfigModel:
    """Load and validate configuration from a JSON file.

    Args:
        filename: Path to the JSON configuration file.

    Returns:
        An instance of `ConfigModel` with validated configuration values.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        pydantic.ValidationError: If the data fails model validation.
    """
    with open(filename, "r") as file:
        lines = [line for line in file if not line.lstrip().startswith('#')]
        file_data = json.loads("".join(lines))

    config_data = ConfigModel.model_validate(file_data)
    return config_data
