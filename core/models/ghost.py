from core.models.entity import Entity
from core.maze import Maze
from core.enums import Direction, GhostMode


class Ghost(Entity):
    """Represents an enemy ghost with autonomous chase/flee behavior."""

    def __init__(self,
                 current_position: tuple[int, int],
                 current_direction: Direction,
                 sprite_id: str,
                 maze_reference: Maze,
                 spawn_position: tuple[int, int],
                 current_mode: GhostMode,
                 ghost_id: int,
                 ) -> None:
        """Initializes the ghost with its starting mode and identity."""
        super().__init__(
            current_position,
            current_direction,
            sprite_id,
            maze_reference,
            spawn_position
        )
        self.current_mode: GhostMode = current_mode
        self.ghost_id: int = ghost_id
        self.target_position: tuple[int, int] = spawn_position

    def get_next_move(self, player_position: tuple[int, int]) -> Direction:
        """Calculates the next direction to move based on the current mode."""
        ...

    def change_mode(self, new_mode: GhostMode) -> None:
        """Changes the ghost's current behavior mode."""
        self.current_mode = new_mode

    def respawn(self) -> None:
        """Resets the ghost to its spawn point and returns it to chase mode."""
        super().respawn()
        self.current_mode = GhostMode.CHASE
