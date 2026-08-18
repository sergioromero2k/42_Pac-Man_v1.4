class Config:
    """Holds the game's configuration values loaded from a config file."""

    def __init__(
            self,
            lives: int,
            pacgum_points: int,
            super_pacgum_points: int,
            ghost_points: int,
            seed: int,
            max_time: int,
            levels: list[tuple[int, int]],
            highscore_filename: str
            ) -> None:
        """Initializes the game configuration with the given values."""
        self.lives: int = lives
        self.pacgum_points: int = pacgum_points
        self.super_pacgum_points: int = super_pacgum_points
        self.ghost_points: int = ghost_points
        self.seed: int = seed
        self.max_time: int = max_time
        self.levels: list[tuple[int, int]] = levels
        self.highscore_filename: str = highscore_filename
