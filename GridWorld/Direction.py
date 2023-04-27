from __future__ import annotations

from typing import Tuple
from enum import Enum

from .Position import Position

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


    def to_position(self) -> Position:
        if self == Direction.UP:      return Position(0,-1)
        elif self == Direction.DOWN:  return Position(0,1)
        elif self == Direction.LEFT:  return Position(-1,0)
        elif self == Direction.RIGHT: return Position(1,0)
        
        raise SystemError(f'Error, invalid direction received: {self}')
    
    def opposite(self) -> Direction:
        if self == Direction.UP:      return Direction.DOWN
        elif self == Direction.DOWN:  return Direction.UP
        elif self == Direction.LEFT:  return Direction.LEFT
        elif self == Direction.RIGHT: return Direction.RIGHT
        
        raise SystemError(f'Error, invalid direction received: {self}')