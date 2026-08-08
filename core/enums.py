from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


class GhostMode(Enum):
    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()


class GamePhase(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAMEOVER = auto()
    VICTORY = auto()


class FlagTypes(Enum):
    INVINCIBILITY = auto()
    FROZEN_GHOSTS = auto()
    INCREASED_SPEED = auto()
