from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Holds the game's configuration values loaded from a config file."""

    lives: int
    pacgum_points: int
    super_pacgum_points: int
    ghost_points: int
    seed: int
    max_time: int
    levels: list[tuple[int, int]]
    highscore_filename: str
