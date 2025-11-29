from enum import Enum, StrEnum, auto


class Direction(StrEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @staticmethod
    def from_str(label):
        lower = label.lower()
        if lower in map(str, Direction):
            return Direction(lower)
        if lower == 'z':
            return Direction.UP
        if lower == 's':
            return Direction.DOWN
        if lower == 'q':
            return Direction.LEFT
        if lower == 'd':
            return Direction.RIGHT
        raise ValueError(f"Invalid direction: {label}")


class Status(Enum):
    ALIVE = 0
    DEAD = 1
    GREEN = 2
    RED = 3


class Tile(StrEnum):
    EMPTY = '0'
    HEAD = 'H'
    BODY = 'S'
    GREEN = 'G'
    RED = 'R'
