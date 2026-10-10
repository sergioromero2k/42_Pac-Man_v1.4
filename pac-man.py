from core.config_loader import ConfigLoader


def main() -> None:
    """Load the config and print a summary."""
    config = ConfigLoader.load_config("config.json")
    print(f"Lives: {config.lives}, levels: {len(config.levels)}")


if __name__ == "__main__":
    main()
