from __future__ import annotations
from typing import List, Tuple
from enum import IntEnum
from random import randint
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])

DIR = [
    Position(0,1),
    Position(0,-1),
    Position(1,0),
    Position(-1,0),
    Position(1,1),
    Position(1,-1),
    Position(-1,1),
    Position(-1,-1),
]

class Action(IntEnum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3

    def to_position(self) -> Position:
        if self == Action.Up: return Position(0, -1)
        if self == Action.Down: return Position(0, 1)
        if self == Action.Left: return Position(-1, 0)
        if self == Action.Right: return Position(1, 0)

        raise SystemError(f'Unsupported action type: {self}.')
    
    @staticmethod
    def from_int(num: int) -> Action:
        if num == 0: return Action.Up
        if num == 1: return Action.Down
        if num == 2: return Action.Left
        if num == 3: return Action.Right

        raise SystemError(f'Unsupported integer to convert to action: {num}.')

class Tile(IntEnum):
    Empty = 0
    Block = 1
    Hazard = 2
    Positive_Reward = 3
    Negative_Reward = 4

    def to_str(self) -> str:
        if self == Tile.Empty: return  '.'
        if self == Tile.Block: return  'X'
        if self == Tile.Hazard: return '^'
        if self == Tile.Positive_Reward: return '+'
        if self == Tile.Negative_Reward: return '-'

        raise SystemError(f'Unsupported tile type: {self}.')

class GridWorld:
    BASE_REWARD = -1
    HAZARD_REWARD = -20
    NEGATIVE_REWARD = -20
    GOAL_REWARD = 20

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player = Position(0,self.height-1)

        self.tile_types = len(Tile)
        self.action_space = len(Action)
        
        self.player = Position(0,self.height-1)
        self.grid = [[Tile.Empty for _ in range(self.width)] for __ in range(self.height)]

    def random_grid(self) -> None:
        self.grid = [[Tile.Empty for _ in range(self.width)] for __ in range(self.height)]
        rand_x = randint(1, self.width-2)
        rand_y = randint(1, self.height-2)

        self.grid[rand_y][rand_x] = Tile.Block
        self.player = Position(0,self.height-1)

        self.grid[0][self.width-1] = Tile.Positive_Reward
        self.grid[1][self.width-1] = Tile.Negative_Reward

    def reset(self) -> None:
        self.player = Position(0,self.height-1)

    def out_of_bounds(self, pos: Position) -> bool:
        return (
            pos.x < 0 or 
            pos.x >= self.width or
            pos.y < 0 or
            pos.y >= self.height
        )

    def render(self) -> None:
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if self.player.x == x and self.player.y == y:
                    line += '@'
                else:
                    line += self.grid[y][x].to_str()
            print(line)

    def __get(self, direction: Position) -> Tile:
        new_pos = Position(direction.x + self.player.x, direction.y + self.player.y)

        if self.out_of_bounds(new_pos):
            return Tile.Block
        else:
            return self.grid[new_pos.y][new_pos.x]

    def observation(self) -> int:
        return int(''.join(str(int(self.__get(d)))for d in DIR))
    
    def random_action(self) -> Action:
        return Action.from_int(randint(0, self.action_space-1))
    
    def step(self, a: int) -> Tuple[float, bool]:
        # reward, and if the simulation is done or not
        a_mod =  Action.from_int(a).to_position()
        new_player_position = Position(self.player.x + a_mod.x, self.player.y + a_mod.y)

        if self.out_of_bounds(new_player_position):
            return self.NEGATIVE_REWARD, False
        
        tile = self.grid[new_player_position.y][new_player_position.x]
        if tile == Tile.Hazard:          return self.HAZARD_REWARD, True
        if tile == Tile.Positive_Reward: return self.GOAL_REWARD, True
        if tile == Tile.Negative_Reward: return self.NEGATIVE_REWARD, True

        if tile != Tile.Block:
            self.player = new_player_position
    
        return self.BASE_REWARD, False

