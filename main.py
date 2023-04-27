# from GDM.GridGraph import GridGraph
# from GDM.utility import *
# from GDM import Policy

from random import choice, seed
from itertools import combinations

from GridWorld import Policy, GridWorld

seed(0)


world = GridWorld(4,3)
pi = Policy()

i = 0
world.print()
while not world.make_move(pi) and i < 10:
    print('\n=============================\n')
    world.print()
    i += 1

print('\n=============================\n')

# def __build_grid_world(MAX_X, MAX_Y) -> Tuple[str, GridGraph]:
#     g = GridGraph() 

#     # create nodes
#     for y in range(MAX_Y):
#         for x in range(MAX_X):
#             # ignore the blank position
#             if y == 1 and x == 1:
#                 continue

#             # create node and its reward
#             src = f'{y}_{x}'
#             if x == MAX_X - 1 and y == MAX_Y - 1:
#                 g.add_default_node(src, reward=1, terminal=True)
#             elif x == MAX_X - 1 and y == MAX_Y - 2:
#                 g.add_default_node(src, reward=-1.0, terminal=True)
#             else:
#                 g.add_default_node(src, reward=-0.04)

#     # create edges
#     for src in g.nodes:
#         # get name
#         y, x = [int(i) for i in src.split('_')]

#         # create left connection
#         if x - 1 >= 0 and not (x - 1 == 1 and y == 1):
#             tgt = f'{y}_{x-1}'
#             g.add_default_edge(src, tgt, [(tgt, 1.0)])

#         # create right connection
#         if x + 1 < MAX_X and not (x + 1 == 1 and y == 1):
#             tgt = f'{y}_{x+1}'
#             g.add_default_edge(src, tgt, [(tgt, 1.0)])

#         # create up connection
#         if y - 1 >= 0 and not (x == 1 and y - 1 == 1):
#             tgt = f'{y-1}_{x}'
#             g.add_default_edge(src, tgt, [(tgt, 1.0)])

#         # create down connection
#         if y + 1 < MAX_Y and not (x == 1 and y + 1 == 1):
#             tgt = f'{y+1}_{x}'
#             g.add_default_edge(src, tgt, [(tgt, 1.0)])

#     return '0_0', g

# def __display_utility_table(G, MAX_X, MAX_Y):
#     print()
#     print('--------' * MAX_X + '-')
#     for y in reversed(range(MAX_Y)):
#         out = '| '
#         for x in range(MAX_X):
#             if x == 1 and y == 1:
#                 out += '      |'
#             else:
#                 key = f'{y}_{x}'
#                 out +=  '{:.2f} | '.format(G.get_node(key).utility)
        
#         print(out)
#         print('--------' * MAX_X + '-')



# start, G = __build_grid_world(4, 3)
# possible_differences = ((1,0),(-1,0),(0,1),(0,-1))
# pi = {

# states = list((s,) for s in possible_differences)
# states += list(combinations(possible_differences, 2))
# states += list(combinations(possible_differences, 3))
# states += list(combinations(possible_differences, 4))

# for s in states:
#     pi[s] = choice(s)
#     print(f'{s}: {pi[s]}')
# print(pi)

# for node in G.nodes:
#     x, y = get_xy(node)
#     neighbor_diffs = []
#     for neighbor in G.neighbors(node):
#         nx, ny = get_xy(neighbor)
#         if nx > x: 
#             neighbor_diffs.append((1,0))
#         elif nx < x:
#             neighbor_diffs.append(((-1,0)))
#         elif ny > y:
#             neighbor_diffs.append((0,1))
#         else:
#             neighbor_diffs.append((0,-1))

#     key = ','.join(str(dif) for dif in neighbor_diffs)
#     print(key)

# pi = ADP.policy_iteration(G, 0.6)
# print(pi)

# states, rewards = run_policy(G, start, pi, 30)
# __display_utility_table(G, 4, 3)
