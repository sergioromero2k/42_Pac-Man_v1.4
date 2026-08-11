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
                 total_score: int,
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
        self.desired_direction: Direction = Direction.NONE

    def handle_input(self, direction: Direction) -> None:
        """Stores the direction the player intends to move towards."""
        self.desired_direction = direction

    def lose_life(self) -> None:
        """Decreases the player's remaining lives by one."""
        self.remaining_lives -= 1

    def respawn_at_maze_center(self) -> None:
        """Respawns the player at the center of the current maze."""
        self.spawn_position = self.maze_reference.get_center_position()
        self.respawn()

    def has_lives_remaining(self) -> bool:
        """Returns True if the player still has lives left."""
        return self.remaining_lives > 0

    def add_life(self) -> None:
        """Increases the player's remaining lives by one."""
        self.remaining_lives += 1
