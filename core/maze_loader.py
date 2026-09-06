from mazegenerator.mazegenerator import MazeGenerator
from core.maze import Maze

BIT_DELTAS = [
    (1, 0, -1),
    (2, 1, 0),
    (4, 0, 1),
    (8, -1, 0)
]


class MazeLoaderError(Exception):
    """Raised when the external maze generator fails."""


class MazeLoader:
    """Adapts the external A-Maze-ing package to the project's Maze format."""

    @staticmethod
    def generate_maze(size: tuple[int, int], seed: int) -> Maze:
        """Generates a Maze using the external generator, in our own format."""
        try:
            maze_gen = MazeGenerator(size=size, perfect=False, seed=seed)
        except Exception as e:
            raise MazeLoaderError(f"Maze generation failed: {e}")

        original_maze = maze_gen.maze
        room_width, room_height = size

        final_height = room_height * 2 + 1
        final_width = room_width * 2 + 1

        walls = {(x, y) for x in range(final_width)
                 for y in range(final_height)}
        paths: set[tuple[int, int]] = set()

        for ry in range(room_height):
            for rx in range(room_width):
                bits = original_maze[ry][rx]
                cx, cy = 2 * rx + 1, 2 * ry + 1
                paths.add((cx, cy))
                walls.discard((cx, cy))
                for bit, dx, dy in BIT_DELTAS:
                    if not (bits & bit):
                        neighbor = (cx + dx, cy + dy)
                        paths.add(neighbor)
                        walls.discard(neighbor)

        return Maze(walls, paths, final_width, final_height)
