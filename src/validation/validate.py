import json
from typing import Any

from pydantic import (
    BaseModel, Field, ConfigDict, field_validator,
    ValidatorFunctionWrapHandler, ValidationInfo
)


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
    model_config = ConfigDict(extra="forbid")

    highscore_filename: str = "scores.json"
    level: list[int] = []
    width: int = Field(ge=14, le=40, default=16)
    height: int = Field(ge=10, le=40, default=10)
    lives: int = Field(ge=1, default=3)
    pacgum: int = Field(ge=0, default=160)
    points_per_pacgum: int = Field(ge=0, default=10)
    points_per_super_pacgum: int = Field(ge=0, default=50)
    points_per_ghost: int = Field(ge=0, default=200)
    seed: int = Field(ge=0, default=42)
    level_max_time: int = Field(ge=1, default=90)

    @field_validator(
        "width", "height", "lives", "pacgum", "points_per_pacgum",
        "points_per_super_pacgum", "points_per_ghost", "seed",
        "level_max_time",
        mode="wrap",
    )
    @classmethod
    def _fallback_to_default(
        cls,
        v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo,
      ) -> Any:
        """
        Fall back to the field's default on invalid type/out-of-range value.
        """
        try:
            return handler(v)
        except Exception:
            field_name = info.field_name
            assert field_name is not None
            print(f"invalide value for '{field_name}', clamp to defalut")
            return cls.model_fields[field_name].default


def validation(filename: str) -> ConfigModel:
    """Load and validate configuration from a JSON file.

    Args:
        filename: Path to the JSON configuration file.

    Returns:
        An instance of `ConfigModel` with validated configuration values.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        pydantic.ValidationError: If the data fails model validation (e.g.
            extra keys, wrong types on non-fallback fields).
    """
    with open(filename, "r") as file:
        lines = [line for line in file if not line.lstrip().startswith("//")]
        file_data = json.loads("".join(lines))

    config_data = ConfigModel.model_validate(file_data)
    return config_data
