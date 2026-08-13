import json

from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    highscore_filename: str
    level: list[int]
    width: int = Field(ge=14)
    height: int = Field(ge=10)
    lives: int = Field(ge=1)
    pacgum: int
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    seed: int = Field(ge=0)
    level_max_time: int = Field(ge=1)


def validation(filename: str) -> ConfigModel:
    with open(filename, "r") as file:
        file_data = json.load(file)
    config_data = ConfigModel.model_validate(file_data)
    return config_data
