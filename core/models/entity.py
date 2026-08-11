from core.enums import Direction, DIRECTION_DELTAS
from core.maze import Maze


class Entity:
    """Base class for any object that lives in the maze and can be drawn."""

    def __init__(
            self,
            current_position: tuple[int, int],
            current_direction: Direction,
            sprite_id: str,
            maze_reference: Maze,
            spawn_position: tuple[int, int]
            ) -> None:
        self.current_position: tuple[int, int] = current_position
        self.current_direction: Direction = current_direction
        self.sprite_id: str = sprite_id
        self.maze_reference: Maze = maze_reference
        self.spawn_position: tuple[int, int] = spawn_position

    def move(self, direction: Direction) -> bool:
        """Attempts to move in the given direction,
        returns True if successful."""
        dx, dy = DIRECTION_DELTAS[direction]

        current_x, current_y = self.current_position
        new_position = (current_x + dx, current_y + dy)
        self.current_direction = direction

        if self.maze_reference.is_path(new_position):
            self.current_position = new_position
            return True

        return False

    def get_position(self) -> tuple[int, int]:
        """Returns the entity's current position."""
        return self.current_position

    def get_sprite(self) -> str:
        """Returns the entity's current sprite identifier."""
        return self.sprite_id

    def respawn(self) -> None:
        """Resets the entity's position to its spawn point
        and stops movement."""
        self.current_position = self.spawn_position
        self.current_direction = Direction.NONE
