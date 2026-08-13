from core.models.entity import Entity
from core.maze import Maze
from core.enums import Direction, GhostMode, DIRECTION_DELTAS


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

        if self.current_mode == GhostMode.EATEN:
            self.target_position = self.spawn_position
        else:
            self.target_position = player_position

        best_direction = Direction.NONE
        best_distance: int | None = None

        for direction, (dx, dy) in DIRECTION_DELTAS.items():
            next_position = (
                self.current_position[0] + dx, self.current_position[1] + dy)

            if not self.maze_reference.is_path(next_position):
                continue

            distance = (
                abs(next_position[0] - self.target_position[0])
                + abs(next_position[1] - self.target_position[1])
            )

            is_better = (
                best_distance is None
                or (
                    self.current_mode == GhostMode.FRIGHTENED
                    and distance > best_distance)
                or (
                    self.current_mode != GhostMode.FRIGHTENED
                    and distance < best_distance)
            )

            if is_better:
                best_distance = distance
                best_direction = direction

        return best_direction

    def change_mode(self, new_mode: GhostMode) -> None:
        """Changes the ghost's current behavior mode."""
        self.current_mode = new_mode

    def respawn(self) -> None:
        """Resets the ghost to its spawn point and returns it to chase mode."""
        super().respawn()
        self.current_mode = GhostMode.CHASE
