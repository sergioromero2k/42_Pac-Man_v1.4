from core.config import Config
import json

DEFAULT_LIVES = 3
DEFAULT_PACGUM_POINTS = 10
DEFAULT_SUPER_PACGUM_POINTS = 50
DEFAULT_GHOST_POINTS = 200
DEFAULT_SEED = 42
DEFAULT_MAX_TIME = 90
DEFAULT_LEVELS = [(20, 10)] * 10
DEFAULT_HIGHSCORE_FILENAME = "data/highscore.json"


class ConfigLoader:
    """Loads and validates the game configuration from a JSON file."""

    @staticmethod
    def load_config(file_path: str) -> Config:
        """Loads, parses and validates the config file, returning a Config."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            print("[Warning] Config file not found. Using default values.")
            return Config(
                lives=3,
                pacgmun_points=10,
                super_pacgum_points=50,
                ghost_points=200,
                seed=42,
                max_time=90,
                levels=[(20, 10)] * 10,
                highscore_filename="data/highscore.json"
            )

        content = ConfigLoader.remove_comments(content)

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"[Warning Invalid JSON: {e}. Using default values.]")
            return Config(
                lives=DEFAULT_LIVES,
                pacgum_points=DEFAULT_PACGUM_POINTS,
                super_pacgum_points=DEFAULT_SUPER_PACGUM_POINTS,
                ghost_points=DEFAULT_GHOST_POINTS,
                seed=DEFA

            )

        lives_raw = data.get("lives", 3)
        lives = lives_raw if isinstance(lives_raw, int) else 3

        pacgmun_points_raw = data.get("pacgmun_points", 3)
        pacgmun_points = pacgmun_points_raw if isinstance(
            pacgmun_points_raw, int) else 10

        super_pacgum_points_raw = data.get("super_pacgum_points", 3)
        super_pacgum_points = super_pacgum_points_raw if isinstance(
            super_pacgum_points_raw, int) else 50

        ghost_points_raw = data.get("ghost_points", 200)
        ghost_points = ghost_points_raw if isinstance(
            ghost_points_raw, int) else 200

        seed_raw = data.get("seed", 42)
        seed = seed_raw if isinstance(seed_raw, int) else 42

        max_time_raw = data.get("max_time", 90)
        max_time = max_time_raw if isinstance(
            max_time_raw, list[tuple[int, int]]) else [(20, 10)] * 10

        levels_raw = data.get("levels", 90)
        levels = levels_raw if isinstance(levels_raw, int) else 90

        max_time_raw = data.get("max_time", 90)
        max_time = max_time_raw if isinstance(max_time_raw, int) else 90

        return Config(
            lives=lives,
            pacgum_points=pacgmun_points,
            super_pacgum_points=super_pacgum_points,
            ghost_points=ghost_points,
            seed=seed,
            max_time=max_time,
            levels=...,
            highscore_filename=...
        )



    @staticmethod
    def remove_comments(content: str) -> str:
        """Removes comment lines (starting with #) from the raw file content."""
        lines = content.splitlines()
        valid_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("#"):
                valid_lines.append(line)
        return "\n".join(valid_lines)
    
