from __future__ import annotations
from typing import Dict, List, Tuple

from GDM import ADP
from GDM.Graph import Graph
from itertools import product

from GridWorld import Tile, Direction, GridWorld, Neighbor
from GridWorld.Policy import Key



def state_to_key(state: Key) -> str:
    return ','.join(s.to_string() for s in state)



G = Graph()
ALL_TILES = [Tile.EMPTY, Tile.NEGATIVE_REWARD, Tile.POSITIVE_REWARD, Tile.BLOCK]

for state in product(ALL_TILES, repeat=4):
    G.add_default_node(
        node_name=state_to_key(state),
        reward=-0.04,
    )

WIDTH = 4
HEIGHT = 3
grid_world = GridWorld(WIDTH, HEIGHT)
G = grid_world.to_graph()