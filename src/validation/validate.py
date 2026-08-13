from pydantic import BaseModel, Filed


class Model(BaseModel):
    highscore_filename: str
    level: list[int]
    width: int = Filed(ge=14)
    height: int = Filed(ge=10)
    lives: int = Filed(ge=1)
    pacgum: int
    points_per_pacgum: int = Filed(ge=0)
    points_per_super_pacgum: int = Filed(ge=0)
    points_per_ghost: int = Filed(ge=0)
    seed: int = Filed(ge=0)
    level_max_time: int = Filed(ge=1)
