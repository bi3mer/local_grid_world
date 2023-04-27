from __future__ import annotations
from collections import namedtuple
from typing import List, Set, Tuple
from GDM.Graph import Graph

from .Position import Position
from .Direction import Direction
from .Tile import Tile
from .Policy import Policy


STATE_TYPE = Tuple[Tile, Tile, Tile, Tile]
Neighbor = namedtuple("Neighbor", ['dir', 'state'])

'''
NOTE: it would be smarter if instead of using a tuple, there was a class 
for this that was hashable.

NOTE: Code would be much more readable if I used a Position class instead
of a tuple. So it could be `new_pos.x` instead of `new_pos[0]` etc.
'''
class GridWorld:
    DIRS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[Tile] = [[Tile.EMPTY for _ in range(width)] for __ in range(height)]
        
        self.grid[height-1][0] = Tile.PLAYER
        self.grid[1][1] = Tile.BLOCK
        self.grid[0][width-1] = Tile.POSITIVE_REWARD
        self.grid[1][width-1] = Tile.NEGATIVE_REWARD

        self.player_pos = Position(0, height-1)

    def get_tile(self, pos: Position) -> Tile:
        if pos.x < 0 or pos.x >= self.width or pos.y < 0 or pos.y >= self.height:
            return Tile.BLOCK
        else:
            return self.grid[pos.y][pos.x]

    def get_state(self, pos: Position) -> STATE_TYPE:
        new_state = []
        for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            d_mod = d.to_position()
            new_pos = Position(pos.x + d_mod.x, pos.y + d_mod.y)
            new_state.append(self.get_tile(new_pos))

        return tuple(new_state)

    def make_move(self, pi: Policy) -> bool:
        # return true if game is over, else false
        move = pi.get(self.get_state()).to_position()
        new_pos = Position(self.player_pos.x + move.y, self.player_pos.x + move.y)

        assert new_pos[0] >= 0
        assert new_pos[0] < self.width
        assert new_pos[1] >= 0
        assert new_pos[1] < self.height
        assert self.grid[new_pos[1]][new_pos[0]] != Tile.BLOCK

        new_state = self.grid[new_pos.y][new_pos.x]
        self.grid[new_pos.y][new_pos.x] = Tile.PLAYER
        self.grid[self.player_pos.y][self.player_pos.x] = Tile.EMPTY
        self.player_pos = new_pos

        return new_state == Tile.POSITIVE_REWARD or new_state == Tile.NEGATIVE_REWARD
            
    def print(self) -> None:
        print('\n'.join(''.join(s.to_string() for s in row) for row in self.grid))

    def reset_player_position(self) -> None:
        self.player_pos = Position(0,0)

    ############################# GDM Support #############################
    def _state_to_string(self, state: STATE_TYPE) -> str:
        return ','.join(s.to_string() for s in state)

    def _neighbors(self, pos: Position) -> List[Position]:
        n = []
        for dir in self.DIRS:
            mod = dir.to_position()
            new_pos = Position(pos.x + mod.x, pos.y + mod.y)

            if new_pos.x >= 0 or pos.x < self.width or pos.y >= 0 or pos.y < self.height:
                n.append(new_pos)

        return n

    def to_graph(self) -> Graph:
        DEFAULT_REWARD = -0.04
        POSITIVE_REWARD = 1.0
        NEGATIVE_REWARD = -1.0
        G = Graph()

        # queue of positions to explore
        queue = [self.player_pos]
        visited: Set[Position] = set()

        while len(queue) > 0:
            pos = queue.pop()
            
            # Default reward unless the tile is  terminal
            reward = DEFAULT_REWARD
            tile = self.grid[pos.y][pos.x]
            if tile == Tile.NEGATIVE_REWARD:
                reward = NEGATIVE_REWARD
            elif tile == Tile.POSITIVE_REWARD:
                reward = POSITIVE_REWARD

            # Get the name of the current state
            state_name = self._state_to_string(self.get_state(pos))

            # If reward is not default, we are at a terminal state
            if reward != DEFAULT_REWARD:
                G.add_default_node(
                    node_name=state_name,
                    reward=reward,
                    terminal=True
                )

                # continue to next position in queue
                continue

            # loop through valid neighbors of the state
            for neighbor_pos in self._neighbors(pos):
                # if the neighbor pos has not been visited, add it to the queue
                # of states we want to vist
                if neighbor_pos not in visited:
                    queue.append(neighbor_pos)

                # Add this neighbor position to the list of neighbors of the 
                # current state
                neighbor_name = self._state_to_string(self.get_state(neighbor_pos))
                G.add_default_edge(state_name, neighbor_name) 
                # TODO: GDM doesn't automatically handle probabilities on add_edge. Meaning,
                # there isn't nay duplicate checking, which is a bug for this implementation
        
