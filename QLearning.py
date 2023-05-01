from __future__ import annotations
from typing import Dict, List

from random import uniform
from tqdm import trange
import numpy as np

from time import sleep

from GridWorld import GridWorld

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
        if state not in self.q_table:
            self.q_table[state] = [uniform(0,1) for _ in range(self.env.action_space)]

        return np.argmax(self.q_table[state])
    
    def __best_q_value(self, state) -> float:
        if state not in self.q_table:
            self.q_table[state] = [uniform(0,1) for _ in range(self.env.action_space)]

        return max(self.q_table[state])

    def train(self, epochs: int):
        for _ in trange(epochs, desc='Training agent', leave=False):
            self.env.reset()
            state = self.env.observation()
            epochs, penalties, reward, = 0, 0, 0
            done = False

            while not done:
                if uniform(0,1) < self.epsilon:
                    action = self.env.random_action()
                else:
                    action = self.__best_action(state)

                reward, done = self.env.step(action) 

                old_value = self.q_table[state][action]
                next_state = self.env.observation()
                next_max = self.__best_q_value(next_state)

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value

                if reward == -10:
                    penalties += 1

                epochs += 1

    def epoch_evaluation(self):
        total_epochs, total_penalties = 0, 0
        episodes = 100

        for _ in trange(episodes, desc='Evaluating agent', leave=False):
            state = self.env.reset()[0]
            epochs, penalties, reward = 0, 0, 0

            
            done = False
            
            while not done:
                action = np.argmax(self.q_table[state])
                state, reward, done, _, _ = self.env.step(action)

                if reward == -10:
                    penalties += 1

                epochs += 1

            total_penalties += penalties
            total_epochs += epochs

        print(f"Results after {episodes} episodes:")
        print(f"Average time steps per episode: {total_epochs / episodes}")
        print(f"Average penalties per episode: {total_penalties / episodes}")

    def visualize_policy_playthrough(self):
        self.env.reset()
        state = self.env.observation()
        done = False

        while not done:
            action = self.__best_action(state)
            reward, done = self.env.step(action)

            print(self.env.render())
            print(f'reward={reward}')
            sleep(0.1)