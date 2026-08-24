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
    def _default_config() -> Config:
        """Returns a Config built entirely from safe default values."""
        return Config(
            lives=DEFAULT_LIVES,
            pacgum_points=DEFAULT_PACGUM_POINTS,
            super_pacgum_points=DEFAULT_SUPER_PACGUM_POINTS,
            ghost_points=DEFAULT_GHOST_POINTS,
            seed=DEFAULT_SEED,
            max_time=DEFAULT_MAX_TIME,
            levels=DEFAULT_LEVELS,
            highscore_filename=DEFAULT_HIGHSCORE_FILENAME
        )

    @staticmethod
    def load_config(file_path: str) -> Config:
        """Loads, parses and validates the config file, returning a Config."""

        # Leer el archivo
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            print("[Warning] Config file not found. Using default values.")
            return ConfigLoader._default_config()

        # Quitar comentarios
        content = ConfigLoader.remove_comments(content)

        # Parsear JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"[Warning Invalid JSON: {e}. Using default values.]")
            return ConfigLoader._default_config()

        # Validar valores
        lives_raw = data.get("lives", DEFAULT_LIVES)
        lives = lives_raw if isinstance(lives_raw, int) else DEFAULT_LIVES

        pacgum_points_raw = data.get("pacgum_points", DEFAULT_PACGUM_POINTS)
        pacgum_points = pacgum_points_raw if isinstance(
            pacgum_points_raw, int) else DEFAULT_PACGUM_POINTS

        super_pacgum_points_raw = data.get(
            "super_pacgum_points",
            DEFAULT_SUPER_PACGUM_POINTS)
        super_pacgum_points = super_pacgum_points_raw if isinstance(
            super_pacgum_points_raw, int) else DEFAULT_SUPER_PACGUM_POINTS

        ghost_points_raw = data.get("ghost_points", DEFAULT_GHOST_POINTS)
        ghost_points = ghost_points_raw if isinstance(
            ghost_points_raw, int) else DEFAULT_GHOST_POINTS

        seed_raw = data.get("seed", DEFAULT_SEED)
        seed = seed_raw if isinstance(seed_raw, int) else DEFAULT_SEED

        max_time_raw = data.get("max_time", DEFAULT_MAX_TIME)
        max_time = max_time_raw if isinstance(
            max_time_raw, int) else DEFAULT_MAX_TIME

        levels_raw = data.get("levels", DEFAULT_LEVELS)
        levels = []

        if isinstance(levels_raw, list):
            for level in levels_raw:
                if (
                    isinstance(level, list)
                    and len(level) == 2
                    and isinstance(level[0], int)
                    and isinstance(level[1], int)
                ):
                    levels.append((level[0], level[1]))

        if not levels:
            levels = DEFAULT_LEVELS

        highscore_filename_raw = data.get(
            "highscore_filename",
            DEFAULT_HIGHSCORE_FILENAME
        )

        highscore_filename = (
            highscore_filename_raw
            if isinstance(highscore_filename_raw, str)
            else DEFAULT_HIGHSCORE_FILENAME
        )

        # Construir Config
        return Config(
            lives=lives,
            pacgum_points=pacgum_points,
            super_pacgum_points=super_pacgum_points,
            ghost_points=ghost_points,
            seed=seed,
            max_time=max_time,
            levels=levels,
            highscore_filename=highscore_filename
        )

    @staticmethod
    def remove_comments(content: str) -> str:
        """Removes comment lines
        (starting with #) from the raw file content."""
        lines = content.splitlines()
        valid_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("#"):
                valid_lines.append(line)
        return "\n".join(valid_lines)
