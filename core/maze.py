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
        """Returns True if the given position is a wall."""
        return pos in self.walls

    def is_path(self, pos: tuple[int, int]) -> bool:
        """Returns True if the given position is a walkable path."""
        return pos in self.paths

    def _nearest_path(self, target: tuple[int, int]) -> tuple[int, int]:
        """Returns the walkable tile closest to target."""
        tx, ty = target
        return min(self.paths,
                   key=lambda p: (abs(p[0] - tx) + abs(p[1] - ty), p))

    def get_center_position(self) -> tuple[int, int]:
        """Returns the walkable tile closest to the maze center."""
        return self._nearest_path(
            (self.maze_width//2), (self.maze_height // 2))

    def get_corners(self) -> list[tuple[int, int]]:
        """Returns the four corner positions of the maze."""
        return [
            (0, 0),
            (self.maze_width - 1, 0),
            (0, self.maze_height - 1),
            (self.maze_width - 1, self.maze_height - 1),
        ]
