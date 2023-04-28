import gymnasium as gym
from time import sleep  

from QLearning import QLearning

def print_frames(frames):
    for i, frame in enumerate(frames):
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)

env: gym.Env = gym.make("Taxi-v3", render_mode='ansi')
env.reset()

q_learning = QLearning(env)
q_learning.train(50000)
q_learning.epoch_evaluation()
q_learning.visualize_policy_playthrough()