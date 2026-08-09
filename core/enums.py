from enum import Enum, auto


class Direction(Enum):
    """Represents the four cardinal movement directions,
    plus a stopped state.
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


DIRECTION_DELTAS: dict[Direction, tuple[int, int]] = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
    Direction.NONE: (0, 0)
}


class GhostMode(Enum):
    """Represents the current behavior mode of a ghost."""
    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()


class GamePhase(Enum):
    """Represents the current phase of the game."""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAMEOVER = auto()
    VICTORY = auto()


class FlagTypes(Enum):
    """Represents the cheat mode toggles available in the game."""
    INVINCIBILITY = auto()
    FROZEN_GHOSTS = auto()
    INCREASED_SPEED = auto()
