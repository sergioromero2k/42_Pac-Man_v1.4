class Maze:
    """Represents the maze layout for a single level, with walls and paths."""

    def __init__(
            self,
            walls: set[tuple[int, int]],
            paths: set[tuple[int, int]],
            maze_width: int,
            maze_height: int
            ) -> None:
        self.walls: set[tuple[int, int]] = walls
        self.paths: set[tuple[int, int]] = paths
        self.maze_width: int = maze_width
        self.maze_height: int = maze_height

    def is_wall(self, pos: tuple[int, int]) -> bool:
        return pos in self.walls

    def is_path(self, pos: tuple[int, int]) -> bool:
        return pos in self.paths

    def get_center_position(self) -> tuple[int, int]:
        ...

    def get_corners(self) -> list[tuple[int, int]]:
        ...
