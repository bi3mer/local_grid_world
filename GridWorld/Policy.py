from typing import Dict, Tuple, List
from itertools import product
from random import random, seed

from .Direction import Direction
from .Tile import Tile

Key = Tuple[Tile, Tile, Tile, Tile]
Utility = Tuple[float, float, float, float]

class Policy:
    IMPOSSIBLE_UTILITY = -10000000
    DIRS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    
    def __init__(self, _seed: int = 0):
        '''
        It would be smart to support depth so you could 
        '''
        seed(_seed)
        self.states: Dict[Key, Utility] = {}

        ALL_STATES = [Tile.EMPTY, Tile.NEGATIVE_REWARD, Tile.POSITIVE_REWARD, Tile.BLOCK]
        
        # 80 possible states with only block, block, block, block skipped
        for s in product(ALL_STATES, repeat=4):
            utility: List[Direction] = []
            for i in range(self.DIRS):
                if s[i] != Tile.BLOCK:
                    utility.append(random())
                else:
                    utility.append(self.IMPOSSIBLE_UTILITY)

            self.states[s] = tuple(utility)

    def get(self, state: Key) -> Direction:
        best_dir = Direction.UP
        best_utility = -1

        for i, dir in enumerate(self.DIRS):
            if self.states[state][i] > best_utility:
                best_utility = self.states[state][i]
                best_dir = dir

        return best_dir
    
    def reset_utility(self) -> None:
        for s in self.states:
            for i in range(len(self.DIRS)):
                if self.states[s][i] != self.IMPOSSIBLE_UTILITY:
                    self.states[s][i] = random()

    def update_utility(self, state: Key, utility: Utility) -> None:
        self.states[state] = utility