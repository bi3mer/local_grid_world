from GridWorld import GridWorld
from QLearning import QLearning

env = GridWorld(10,10)
env.random_grid()

q = QLearning(env)
q.train(1_000)
q.visualize_policy_playthrough()

print('Changing grid!')
print()
env.random_grid()
env.render()
q.visualize_policy_playthrough()