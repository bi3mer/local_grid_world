from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Node:
    name: Tuple[int, int]
    reward: float
    utility: float
    is_terminal: bool
    up: bool
    down: bool
    left: bool
    right: bool

    @property
    def policy_key(self) -> List[Tuple[int, int]]:
        return_val = []

        if self.up:    return_val.append((0,-1))
        if self.down:  return_val.append((0,1))
        if self.right: return_val.append((1,0))
        if self.left:  return_val.append((-1,0))

        return return_val
    