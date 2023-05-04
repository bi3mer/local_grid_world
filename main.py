from GridWorld import GridWorld
from QLearning import QLearning

env = GridWorld(5,5)
env.random_grid()

q = QLearning(env)
q.train(100)
q.visualize_policy_playthrough()

env.random_grid()
print('Changing grid!')
print()
env.render()
q.visualize_policy_playthrough()