import json
from core.config import Config
from typing import Any


# Defaults value
DEFAULT_LIVES = 3
DEFAULT_POINTS_PER_PACGUM = 10
DEFAULT_POINTS_PER_SUPER_PACGUM = 50
DEFAULT_POINTS_PER_GHOST = 200
DEFAULT_SEED = 42
DEFAULT_LEVEL_MAX_TIME = 90
DEFAULT_LEVELS = [(20, 10)] * 10
DEFAULT_HIGHSCORE_FILENAME = "data/highscore.json"

# Max y Min
MIN_LIVES, MAX_LIVES = 1, 99
MIN_POINTS, MAX_POINTS = 0, 100_000
MIN_SEED, MAX_SEED = 1, 2_147_483_647
MIN_LEVEL_TIME, MAX_LEVEL_TIME = 1, 3_600
MIN_LEVEL_SIZE, MAX_LEVEL_SIZE = 5, 50
MAX_LEVELS = 100
MAX_FILENAME_LENGTH = 255
MAX_FILE_SIZE = 1_000_000


def _warn(message: str) -> None:
    """Prints a configuration warning."""
    print(f"[Warning] {message}")


class ConfigLoader:
    """Loads and validates the game configuration from a JSON file.

    It never raises: any problem is reported with a warning and replaced
    by a safe default value, so a bad config file cannot stop the game.
    """

    @staticmethod
    def _default_config() -> Config:
        """Returns a Config built entirely from safe default values."""
        return Config(
            lives=DEFAULT_LIVES,
            points_per_pacgum=DEFAULT_POINTS_PER_PACGUM,
            points_per_super_pacgum=DEFAULT_POINTS_PER_SUPER_PACGUM,
            points_per_ghost=DEFAULT_POINTS_PER_GHOST,
            seed=DEFAULT_SEED,
            level_max_time=DEFAULT_LEVEL_MAX_TIME,
            levels=list(DEFAULT_LEVELS),
            highscore_filename=DEFAULT_HIGHSCORE_FILENAME
        )

    @staticmethod
    def _get_int(
        data: dict[str, Any], key: str, default: int,
        minimum: int, maximum: int
    ) -> int:
        """Returns data[key] if it is an int >= minimum, else default."""
        if key not in data:
            _warn(f"Missing key '{key}'. Using default: {default}")
            return default
        value = data[key]
        if isinstance(value, bool) or not isinstance(value, int):
            _warn(f"'{key}' must be an integer, got {value!r}. "  # 'hola'
                  f"Using default: {default}")
            return default
        if not minimum <= value <= maximum:
            _warn(f"'{key}' must be between {minimum} and {maximum}, "
                  f"got {value}. Using default: {default}")
            return default
        return value

    @staticmethod
    def _get_str(data: dict[str, Any], key: str, default: str) -> str:
        """Returns data[key] if it is a non-empty string, else default."""
        if key not in data:
            _warn(f"Missing key '{key}'. Using default: {default}")
            return default
        value = data[key]
        if (
            not isinstance(value, str)
            or not value.strip()
            or len(value) > MAX_FILENAME_LENGTH
            or "\0" in value
        ):
            _warn(f"'{key}' must be a non-empty file name of at most "
                  f"{MAX_FILENAME_LENGTH} characters. "
                  f"Using default: {default}")
            return default
        return value

    @staticmethod
    def _get_levels(data: dict[str, Any]) -> list[tuple[int, int]]:
        """Returns the valid (width, height) levels, or the defaults."""
        if "levels" not in data:
            _warn("Missing key 'levels'. Using default levels.")
            return list(DEFAULT_LEVELS)
        raw = data["levels"]
        if not isinstance(raw, list):
            _warn("'levels' must be a list of [width, height]. "
                  "Using default levels.")
            return list(DEFAULT_LEVELS)

        levels: list[tuple[int, int]] = []
        for index, level in enumerate(raw, start=1):
            if (
                isinstance(level, list)
                and len(level) == 2
                and all(
                    isinstance(v, int)
                    and not isinstance(v, bool)
                    and v >= MIN_LEVEL_SIZE
                    for v in level
                )
            ):
                levels.append((level[0], level[1]))
            else:
                _warn(f"Invalid level #{index}: {level!r}. Skipping it.")

        if not levels:
            _warn("No valid levels found. Using default levels.")
            return list(DEFAULT_LEVELS)
        return levels

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

    @staticmethod
    def load_config(file_path: str) -> Config:
        """Loads, parses and validates the config file, returning a Config."""

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except (OSError, UnicodeDecodeError) as error:
            _warn(f"Cannot read '{file_path}': {error}. Using default values.")
            return ConfigLoader._default_config()

        # Quitar comentarios
        content = ConfigLoader.remove_comments(content)

        # Parsear JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"[Warning Invalid JSON: {e}. Using default values.]")
            return ConfigLoader._default_config()

        if not isinstance(data, dict):
            _warn("The config root must be a JSON object. "
                  " Using default values.")
            return ConfigLoader._default_config()

        # Cree un alias, nombre mas corto...
        get_int = ConfigLoader._get_int
        get_levels = ConfigLoader._get_levels
        get_str = ConfigLoader._get_str

        # Validar valores
        return Config(
            lives=get_int(data, "lives", DEFAULT_LIVES, 1),
            pacgum_points=get_int(
                data, "pacgum_points", DEFAULT_PACGUM_POINTS, 0),
            super_pacgum_points=get_int(
                data, "super_pacgum_points",
                DEFAULT_SUPER_PACGUM_POINTS, 0),
            ghost_points=get_int(
                data, "ghost_points", DEFAULT_GHOST_POINTS, 0),
            seed=get_int(data, "seed", DEFAULT_SEED, 1),
            max_time=get_int(data, "max_time", DEFAULT_MAX_TIME, 1),
            levels=get_levels(data),
            highscore_filename=get_str(
                data, "highscore_filename", DEFAULT_HIGHSCORE_FILENAME),
        )
