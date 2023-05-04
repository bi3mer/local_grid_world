from __future__ import annotations
from typing import Dict, List

from random import uniform
from tqdm import trange
import numpy as np

from time import sleep

from GridWorld import GridWorld, Action

class QLearning:
    def __init__(
        self, 
        env: GridWorld,
        alpha:float = 0.1, 
        gamma:float = 0.6, 
        epsilon:float = 0.1,
    ):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: Dict[int, List[float]] = {}

    def __best_action(self, state) -> int:
        return np.argmax(self.q_table[state])
    
    def __best_q_value(self, state) -> float:
        if state not in self.q_table:
            self.q_table[state] = [0 for _ in range(self.env.action_space)]

        return max(self.q_table[state])
    
    def __train_from_solution(self, solution):
        state = self.env.observation()
        R = 10

        for a in solution:
            int_a = int(a)
            if state not in self.q_table:
                self.q_table[state] = [0 for _ in range(self.env.action_space)]

            self.env.step(int_a)
            old_value = self.q_table[state][int_a]

            next_state = self.env.observation()
            next_max = self.__best_q_value(next_state)

            new_value = (1 - self.alpha) * old_value + self.alpha * (R + self.gamma * next_max)
            self.q_table[state][int_a] = new_value

            state = next_state

    def train(self, epochs: int):
        self.env.reset()
        solution = self.env.get_solution()
        for _ in trange(epochs, desc='Cheating!', leave=False):
            self.__train_from_solution(solution)
            self.env.reset()

        for i in trange(epochs, desc='Training agent', leave=False):
            self.env.reset()
            state = self.env.observation()
            done = False

            epsilon = max(self.epsilon, min(0.4, (epochs - i) / (epochs+1)))
            while not done:
                if state not in self.q_table:
                    self.q_table[state] = [0 for _ in range(self.env.action_space)]

                if uniform(0,1) < self.epsilon:
                    action = self.env.random_action()
                else:
                    action = self.__best_action(state)

                reward, done = self.env.step(action) 
                old_value = self.q_table[state][action]

                next_state = self.env.observation()
                next_max = self.__best_q_value(next_state)

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state][int(action)] = new_value

                state = next_state

    def visualize_policy_playthrough(self):
        self.env.reset()
        done = False

        while not done:
            action = self.__best_action(self.env.observation())
            reward, done = self.env.step(action)
            
            print()
            self.env.render()
            print(self.q_table[self.env.observation()])
            print(f'action={Action.from_int(action).to_str()}, reward={reward}')
            sleep(0.1)