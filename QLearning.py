from gymnasium import Env
from random import uniform
from tqdm import trange
import numpy as np

from time import sleep

class QLearning:
    def __init__(
        self, 
        env: Env,
        alpha:float = 0.1, 
        gamma:float = 0.6, 
        epsilon:float = 0.1,
    ):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros([env.observation_space.n, env.action_space.n])

    def train(self, epochs: int):
        for _ in trange(epochs, desc='Training agent', leave=False):
            state = self.env.reset()[0]
            epochs, penalties, reward, = 0, 0, 0
            done = False

            while not done:
                if uniform(0,1) < self.epsilon:
                    action = self.env.action_space.sample()
                else:
                    action = np.argmax(self.q_table[state])

                next_state, reward, done, truncated, info = self.env.step(action) 

                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value

                if reward == -10:
                    penalties += 1

                state = next_state
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
                state, reward, done, truncated, info = self.env.step(action)

                if reward == -10:
                    penalties += 1

                epochs += 1

            total_penalties += penalties
            total_epochs += epochs

        print(f"Results after {episodes} episodes:")
        print(f"Average timesteps per episode: {total_epochs / episodes}")
        print(f"Average penalties per episode: {total_penalties / episodes}")

    def visualize_policy_playthrough(self):
        state = self.env.reset()[0]
        done = False

        while not done:
            action = np.argmax(self.q_table[state])
            state, reward, done, truncated, info = self.env.step(action)

            print(self.env.render())
            print(f'reward={reward}')
            sleep(0.1)