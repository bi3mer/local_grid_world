from enum import Enum

class Tile(Enum):
    EMPTY           = 0
    BLOCK           = 1
    POSITIVE_REWARD = 2
    NEGATIVE_REWARD = 3
    PLAYER          = 4

    def to_string(self):
        if self == Tile.EMPTY:           return '.'
        if self == Tile.BLOCK:           return 'X'
        if self == Tile.POSITIVE_REWARD: return '+'
        if self == Tile.NEGATIVE_REWARD: return '-'
        if self == Tile.PLAYER:          return '@'

        raise SystemError(f'Unexpected state type: {self}.')