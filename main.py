import gymnasium as gym
from time import sleep  

from QLearning import QLearning


env: gym.Env = gym.make("Taxi-v3", render_mode='ansi')
env.reset()

q_learning = QLearning(env)
q_learning.train(50000)
q_learning.epoch_evaluation()
q_learning.visualize_policy_playthrough()