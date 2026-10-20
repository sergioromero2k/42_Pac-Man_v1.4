import json
from core.config import Config
from typing import Any


DEFAULT_LIVES = 3
DEFAULT_PACGUM_POINTS = 10
DEFAULT_SUPER_PACGUM_POINTS = 50
DEFAULT_GHOST_POINTS = 200
DEFAULT_SEED = 42
DEFAULT_MAX_TIME = 90
DEFAULT_LEVELS = [(20, 10)] * 10
DEFAULT_HIGHSCORE_FILENAME = "data/highscore.json"

MIN_LEVEL_SIZE = 3


def _warn(message: str) -> None:
    """Prints a configuration warning."""
    print(f"[Warning] {message}")


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
    def _get_int(
        data: dict[str, Any], key: str, default: int,
        minimum: int
    ) -> int:
        """Returns data[key] if it is an int >= minimum, else default."""
        if key not in data:
            _warn(f"Missing key '{key}'. Using default: {default}")
            return default
        value = data[key]
        if isinstance(value, bool) or not isinstance(value, int):
            _warn(f"'{key}' must be an integer, got {value!r}. "
                  f"Using default: {default}")
            return default
        if value < minimum:
            _warn(f"'{key}' must be >= {minimum}, got {value}. "
                  f"Using default: {default}")
            return default
        return value

    @staticmethod
    def _get_str(data: dict[str, Any], key: str, default: str) -> str:
        """Returns data[key] if it is a non-empty string, else default."""
        if key not in data:
            _warn(f"Missing key '{key}'. Using default: {default}")
            return default
        value = data[key]
        if not isinstance(value, str) or not value.strip():
            _warn(f"'{key}' must be a non-empty string, got {value!r}. "
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
