import enum

__all__ = ["Direction"]


class Direction(enum.Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1
