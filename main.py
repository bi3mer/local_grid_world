# import gymnasium as gym
from GridWorld import GridWorld

from QLearning import QLearning

# env: gym.Env = gym.make("Taxi-v3", render_mode='ansi')
# env.reset()

# q_learning = QLearning(env)
# q_learning.train(50000)
# q_learning.epoch_evaluation()
# q_learning.visualize_policy_playthrough()

env = GridWorld(5,5)
env.random_grid()
env.render()

q = QLearning(env)
q.train(1000)
q.visualize_policy_playthrough()