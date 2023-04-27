from __future__ import annotations
from typing import List, Tuple

from .Direction import Direction
from .State import State
from .Policy import Policy

class GridWorld:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[State] = [[State.EMPTY for _ in range(width)] for __ in range(height)]
        
        self.grid[height-1][0] = State.PLAYER
        self.grid[1][1] = State.BLOCK
        self.grid[0][width-1] = State.POSITIVE_REWARD
        self.grid[1][width-1] = State.NEGATIVE_REWARD

        self.player_pos = (0, height-1)

    def get_state(self) -> Tuple[State, State, State, State]:
        '''
        NOTE: it would be smarter if instead of using a tuple, there was a class 
        for this that was hashable.

        NOTE: Code would be much more readable if I used a Position class instead
        of a tuple. So it could be `new_pos.x` instead of `new_pos[0]` etc.
        '''
        new_state = []
        for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            d_mod = d.to_tuple()
            new_pos = (self.player_pos[0] + d_mod[0], self.player_pos[1] + d_mod[1])

            if (
                new_pos[0] < 0 or 
                new_pos[0] >= self.width or 
                new_pos[1] < 0 or 
                new_pos[1] >= self.height
            ):
                new_state.append(State.BLOCK)
            else:
                new_state.append(self.grid[new_pos[1]][new_pos[0]])

        return tuple(new_state)

    def make_move(self, pi: Policy) -> bool:
        # return true if game is over, else false
        move = pi.get(self.get_state()).to_tuple()
        new_pos = (self.player_pos[0] + move[0], self.player_pos[1] + move[1])

        assert new_pos[0] >= 0
        assert new_pos[0] < self.width
        assert new_pos[1] >= 0
        assert new_pos[1] < self.height
        assert self.grid[new_pos[1]][new_pos[0]] != State.BLOCK

        new_state = self.grid[new_pos[1]][new_pos[0]]
        self.grid[new_pos[1]][new_pos[0]] = State.PLAYER
        self.grid[self.player_pos[1]][self.player_pos[0]] = State.EMPTY
        self.player_pos = new_pos

        return new_state == State.POSITIVE_REWARD or new_state == State.NEGATIVE_REWARD
            

    def print(self) -> None:
        print('\n'.join(''.join(s.to_string() for s in row) for row in self.grid))
