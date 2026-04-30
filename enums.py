from enum import StrEnum, IntEnum


class Direction(IntEnum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def from_str(label):
        lower = label.lower()
        if lower in ['w', 'up']:
            return Direction.UP
        if lower in ['s', 'down']:
            return Direction.DOWN
        if lower in ['a', 'left']:
            return Direction.LEFT
        if lower in ['d', 'right']:
            return Direction.RIGHT
        raise ValueError(f"Invalid direction: {label}")

    def __str__(self):
        return self.name


class Status(StrEnum):
    ALIVE = "alive"
    DEAD = "dead"
    GREEN = "green"
    RED = "red"


class Tile(StrEnum):
    WALL = 'W'
    EMPTY = '0'
    HEAD = 'H'
    BODY = 'S'
    GREEN = 'G'
    RED = 'R'
