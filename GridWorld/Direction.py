from __future__ import annotations

from typing import Tuple
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


    def to_tuple(dir: Direction) -> Tuple:
        if dir == Direction.UP:      return (0,-1)
        elif dir == Direction.DOWN:  return (0,1)
        elif dir == Direction.LEFT:  return (-1,0)
        elif dir == Direction.RIGHT: return (1,0)
        
        raise SystemError(f'Error, invalid direction received: {dir}')