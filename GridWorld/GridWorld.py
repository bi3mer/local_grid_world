from __future__ import annotations
from collections import namedtuple
from typing import List, Set, Tuple, Dict
from GDM.Graph import Graph

from .Position import Position
from .Direction import Direction
from .Tile import Tile
from .Policy import Policy

DEFAULT_REWARD = -0.04
POSITIVE_REWARD = 1.0
NEGATIVE_REWARD = -1.0

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
            tile = self.get_tile(new_pos)
            new_state.append(tile if tile != Tile.PLAYER else Tile.EMPTY)

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

    def _neighbors(self, pos: Position) -> List[Tuple(Direction, Position)]:
        n = []
        for dir in self.DIRS:
            mod = dir.to_position()
            new_pos = Position(pos.x + mod.x, pos.y + mod.y)

            if new_pos.x >= 0 and new_pos.x < self.width and new_pos.y >= 0 and new_pos.y < self.height:
                n.append((dir, new_pos))

        return n
    
    def _add_node(self, G: Graph, tile: Tile, name: str) -> bool:
        # Return true if the node is terminal else false
        reward = DEFAULT_REWARD
        if tile == Tile.NEGATIVE_REWARD:
            reward = NEGATIVE_REWARD
        elif tile == Tile.POSITIVE_REWARD:
            reward = POSITIVE_REWARD

        # If reward is not default, we are at a terminal state
        is_terminal = reward != DEFAULT_REWARD

        # Add the node to the graph
        G.add_default_node(
            node_name=name,
            reward=reward,
            terminal=is_terminal
        )

        return is_terminal

    def to_graph(self) -> Graph:
        G = Graph()

        node_neighbors: Dict[str, Dict[Direction, Set[str]]] = {}

        # queue of positions to explore
        queue = [self.player_pos]
        visited: Set[Position] = set()

        # BFS to get all nodes and their neighbors
        tile = self.grid[self.player_pos.y][self.player_pos.x]
        state_name = self._state_to_string(self.get_state(self.player_pos))
        G.add_default_node(
            node_name=state_name,
            reward=DEFAULT_REWARD,
            terminal=False
        )

        while len(queue) > 0:
            # Get next position from the queue
            pos = queue.pop()
            
            # Get state name and update visited
            state_name = self._state_to_string(self.get_state(pos))
            visited.add(pos)

            # If the state is terminal, go to the next state
            if G.get_node(state_name).is_terminal:
                continue

            # make sure temp data structure is built for the node
            if state_name not in node_neighbors:
                node_neighbors[state_name] = {}

            # loop through valid neighbors of the state
            for direction, neighbor_pos in self._neighbors(pos):
                # if the neighbor pos has not been visited, add it to the queue
                # of states we want to vist
                if neighbor_pos not in visited:
                    queue.append(neighbor_pos)
                
                # Get name of the neighbor
                neighbor_name = self._state_to_string(self.get_state(neighbor_pos))

                # Add this neighbor position to the list of neighbors of the 
                # current state
                if neighbor_pos not in visited and neighbor_name not in G.nodes:
                    tile = self.grid[neighbor_pos.y][neighbor_pos.x]
                    self._add_node(G, tile, neighbor_name)
                    
                # NOTE: could be in the if statement above—I'm sure—but I'm
                # a tad tired right now.
                if neighbor_name not in node_neighbors:
                    node_neighbors[neighbor_name] = {}

                # update the neighbors data structure for both nodes
                if direction not in node_neighbors[state_name]:
                    node_neighbors[state_name][direction] = set()
                node_neighbors[state_name][direction].add(neighbor_name)

                if direction not in node_neighbors[neighbor_name]:
                    node_neighbors[neighbor_name][direction] = set()
                node_neighbors[neighbor_name][direction].add(state_name)
                
        # for every node, build edges with their list of neighbors
        for node in node_neighbors:
            print(node)
            for dir in node_neighbors[node]:
                print('\t', dir, len(node_neighbors[node][dir]))

            # break