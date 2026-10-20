"""Pac-Man entry point (temporary: opens the test window)."""
import sys

from core.config_loader import ConfigLoader
from ui.game_window import run_window


def main() -> None:
    """Load the config and open the game window."""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config.json>")
        return

    config = ConfigLoader.load_config("config.json")
    print(f"Lives: {config.lives}, levels: {len(config.levels)}")
    run_window()


if __name__ == "__main__":
    main()
