class HighScoreEntry:
    """Represents a single entry in the highscore ranking."""
    def __init__(
            self, username: str, score: int) -> None:
        self.username = username
        self.score = score


class HighScoreManager:
    """Loads, saves and manages the persistent highscore ranking."""
    def __init__(
            self, file_path: str, entries: list[HighScoreEntry]) -> None:
        self.file_path: str = file_path 
        self.entries: list[HighScoreEntry] = entries

    def load_from_disk(self) -> None:
        """Loads highscore entries from the JSON file, resetting on error."""
        ...

    def save_to_disk(self) -> None:
        """Writes the current highscore entries to the JSON file."""
        ...

    def add_new_score(self, username: str, score: int) -> bool:
        """Validates and adds a new score, keeping only the top 10."""

        ...

    def keep_only_top_10(self) -> None:
        """Sorts emtries by score and trims the list to the top 10."""
        ...
