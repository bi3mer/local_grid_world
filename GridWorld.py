from __future__ import annotations
from typing import List, Tuple
from enum import IntEnum
from random import randint, choice, random, shuffle
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])

class Action(IntEnum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3

    @staticmethod
    def from_int(num: int) -> Action:
        if num == 0: return Action.Up
        if num == 1: return Action.Down
        if num == 2: return Action.Left
        if num == 3: return Action.Right

        raise SystemError(f'Unsupported integer to convert to action: {num}.')

    def to_position(self) -> Position:
        if self == Action.Up: return Position(0, -1)
        if self == Action.Down: return Position(0, 1)
        if self == Action.Left: return Position(-1, 0)
        if self == Action.Right: return Position(1, 0)

        raise SystemError(f'Unsupported action type: {self}.')
    
    def to_str(self) -> str:
        if self == Action.Up: return 'Up'
        if self == Action.Down: return 'Down'
        if self == Action.Left: return 'Left'
        if self == Action.Right: return 'Right'

        raise SystemError(f'Unsupported action type: {self}.')

class Tile(IntEnum):
    Empty = 0
    Block = 1
    Hazard = 2
    Positive_Reward = 3

    def to_str(self) -> str:
        if self == Tile.Empty: return  '.'
        if self == Tile.Block: return  'X'
        if self == Tile.Hazard: return '^'
        if self == Tile.Positive_Reward: return '+'

        raise SystemError(f'Unsupported tile type: {self}.')

class GridWorld:
    BASE_REWARD = -1
    HAZARD_REWARD = -20
    GOAL_REWARD = 20

    OBSERVATION_SIZE = 4

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
        self.grid[0][self.width-1] = Tile.Positive_Reward

        self.player = Position(0, self.height - 1)
        free_blocks = [Position(0,self.height-1)]

        temp = self.get_solution(dfs=True)
        for a in temp:
            mod = a.to_position()
            new_pos = Position(free_blocks[-1].x + mod.x, free_blocks[-1].y + mod.y)
            free_blocks.append(new_pos)

        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = Position(x, y)
                if pos in free_blocks:
                    continue
                
                rand_number = random()
                if rand_number > 0.8:
                    self.grid[y][x] = Tile.Hazard
                elif rand_number > 0.5:
                    self.grid[y][x] = Tile.Block

        self.grid[0][self.width-1] = Tile.Positive_Reward

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
            print(f'\t{line}')

    def __get(self, direction: Position) -> Tile:
        new_pos = Position(direction.x + self.player.x, direction.y + self.player.y)

        if self.out_of_bounds(new_pos):
            return Tile.Block
        else:
            return self.grid[new_pos.y][new_pos.x]

    def observation(self) -> Tuple[str,...]:
        tiles = []
        for y in range(-self.OBSERVATION_SIZE, self.OBSERVATION_SIZE-1):
            for x in range(-self.OBSERVATION_SIZE, self.OBSERVATION_SIZE-1):
                if y == 0 and x == 0: 
                    continue
                
                tiles.append(self.__get(Position(x, y)).to_str())

        return tuple(tiles)
    
    def random_action(self) -> Action:
        return Action.from_int(randint(0, self.action_space-1))
    
    def step(self, a: int) -> Tuple[float, bool]:
        a_mod =  Action.from_int(a).to_position()
        new_player_position = Position(self.player.x + a_mod.x, self.player.y + a_mod.y)

        if self.out_of_bounds(new_player_position):
            return self.BASE_REWARD, False
        
        tile = self.grid[new_player_position.y][new_player_position.x]
        if tile != Tile.Block:
            self.player = new_player_position

        if tile == Tile.Hazard:          return self.HAZARD_REWARD, True
        if tile == Tile.Positive_Reward: return self.GOAL_REWARD, True
    
        return self.BASE_REWARD, False

    def get_solution(self, dfs=False) -> List[Action]:
        self.reset()
        ACTIONS: List[Action] = [Action.Up, Action.Down, Action.Right, Action.Left]
        queue = [(self.player, [])]
        visited = set()

        while len(queue) > 0:
            if dfs:
                state, actions = queue.pop()
            else:
                state, actions = queue.pop(0)
            
            if state in visited:
                continue
            
            visited.add(state)

            if dfs:
                shuffle(ACTIONS)

            for a in ACTIONS:
                mod = a.to_position()
                new_state = Position(state.x + mod.x, state.y + mod.y)

                new_actions = actions.copy()
                new_actions.append(a)

                if not self.out_of_bounds(new_state):
                    tile = self.grid[new_state.y][new_state.x]
                    if tile == Tile.Positive_Reward:
                        return new_actions
                    elif tile == Tile.Empty:
                        queue.append((new_state, new_actions))

        return []
