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
        self.file_path = file_path 
        self.entries = entries

    def load_from_disk(self) -> None:
        ...

    def save_to_disk(self) -> None:
        ...

    def add_new_score(self, username: str, score: int) -> bool:
        ...

    def keep_only_top_10(self) -> None:
        
        ...
