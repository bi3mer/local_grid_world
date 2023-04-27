from typing import Dict, Tuple, List
from itertools import product
from random import choice, seed

from .Direction import Direction
from .State import State

class Policy:
    def __init__(self, _seed: int = 0):
        '''
        It would be smart to support depth so you could 
        '''
        seed(_seed)

        self.player_pos: Tuple[int, int] = (0,0)
        self.states: Dict[Tuple[State, State, State, State], Direction] = {}

        ALL_STATES = [State.EMPTY, State.NEGATIVE_REWARD, State.POSITIVE_REWARD, State.BLOCK]
        DIRS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        
        # 80 possible states with only block, block, block, block skipped
        for s in product(ALL_STATES, repeat=4):
            valid_directions: List[Direction] = []
            for i, dir in enumerate(DIRS):
                if s[i] != State.BLOCK:
                    valid_directions.append(dir)
            
            if len(valid_directions) > 0:
                self.states[s] = choice(valid_directions) 

    def get(self, state: Tuple[State, State, State, State]) -> Direction:
        return self.states[state]
    
    def reset_player_position(self) -> None:
        self.player_pos = (0,0)

        

    