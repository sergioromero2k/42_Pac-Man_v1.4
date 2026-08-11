from core.models.entity import Entity
from core.maze import Maze
from core.enums import Direction


class Player(Entity):
    """Represents the user-controlled character."""

    def __init__(self,
                 current_position: tuple[int, int],
                 current_direction: Direction,
                 sprite_id: str,
                 maze_reference: Maze,
                 spawn_position: tuple[int, int],
                 remaining_lives: int,
                 total_score: int
                 ) -> None:
        """Initializes the player with its starting stats."""
        super().__init__(
            current_position,
            current_direction,
            sprite_id,
            maze_reference,
            spawn_position
        )
        self.remaining_lives: int = remaining_lives
        self.total_score: int = total_score

    def handle_input(self, direction: Direction) -> None:
        ...

    def lose_life(self) -> None:
        ...

    def respawn_at_maze_center(self) -> None:
        ...

    def has_lives_remaining(self) -> bool:
        ...

    def add_life(self) -> None:
        ...
