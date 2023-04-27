from __future__ import annotations

from typing import Tuple
from enum import Enum

from .Position import Position

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


    def to_position(dir: Direction) -> Position:
        if dir == Direction.UP:      return Position(0,-1)
        elif dir == Direction.DOWN:  return Position(0,1)
        elif dir == Direction.LEFT:  return Position(-1,0)
        elif dir == Direction.RIGHT: return Position(1,0)
        
        raise SystemError(f'Error, invalid direction received: {dir}')