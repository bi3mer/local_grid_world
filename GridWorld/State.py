from enum import Enum

class State(Enum):
    EMPTY           = 0
    BLOCK           = 1
    POSITIVE_REWARD = 2
    NEGATIVE_REWARD = 3
    PLAYER          = 4

    def to_string(self):
        if self == State.EMPTY:           return '.'
        if self == State.BLOCK:           return 'X'
        if self == State.POSITIVE_REWARD: return '+'
        if self == State.NEGATIVE_REWARD: return '-'
        if self == State.PLAYER:          return '@'

        raise SystemError(f'Unexpected state type: {self}.')
        