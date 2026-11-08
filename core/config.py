from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Holds the game's configuration values loaded from a config file."""

    lives: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int
    levels: list[tuple[int, int]]
    highscore_filename: str


"""
Example
config = Config(
    lives=3,
    points_per_pacgum=10,
    points_per_super_pacgum=50,
    points_per_ghost=200,
    seed=123,
    level_max_time=60,
    levels=[
        (10, 5), (15, 8)],
    highscore_filename="highscores.txt"
)
"""
