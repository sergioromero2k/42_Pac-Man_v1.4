from mazegenerator.mazegenerator import MazeGenerator
from core.maze import Maze


class MazeLoaderError(Exception):
    """Raised when the external maze generator fails."""


class MazeLoader:
    """Adapts the external A-Maze-ing package to the project's Maze format."""

    @staticmethod
    def generate_maze(size: tuple[int, int], seed: int) -> Maze:
        """Generates a Maze using the external generator, in our own format."""
        maze_gen = MazeGenerator(size, perfect=False, seed=seed)
        maze_gen.generate(seed=seed)
        original_maze = maze_gen.maze

        room_width, room_height = size

        final_height = room_height * 2 + 1
        final_width = room_width * 2 + 1

        

