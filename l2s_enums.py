from enum import Enum, StrEnum, IntEnum


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def from_str(label):
        lower = label.lower()
        if lower in ['z', 'up']:
            return Direction.UP
        if lower in ['s', 'down']:
            return Direction.DOWN
        if lower in ['q', 'left']:
            return Direction.LEFT
        if lower in ['d', 'right']:
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
