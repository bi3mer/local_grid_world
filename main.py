from GridWorld import GridWorld
from QLearning import QLearning

env = GridWorld(10,10)
env.random_grid()

q = QLearning(env)
q.train(1000)
q.visualize_policy_playthrough()

env.random_grid()
print('Changing grid!')
print()
env.render()
q.visualize_policy_playthrough()