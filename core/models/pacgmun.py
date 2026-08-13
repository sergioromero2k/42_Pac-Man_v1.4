
class Pacgum:
    """Represents a collectible dot in the maze."""
    def __init__(self,
                 pos: tuple[int, int],
                 was_collected: bool,
                 point_value: int,
                 is_super: bool
                 ) -> None:
        """Initializes a pacgmun at a given position with its point value."""
        self.pos: tuple[int, int] = pos
        self.was_collected: bool = False
        self.point_value: int = point_value
        self.is_super: bool = is_super

    def mark_as_collected(self) -> bool:
        """Marks the pacgmun as collected. 
            Returns False if already collected."""
        ...

    def get_point_value(self) -> int:
        """Returns the point value of this pacgmun."""
        ...
