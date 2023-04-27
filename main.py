from GridWorld import Policy, GridWorld

world = GridWorld(4,3)
pi = Policy()

i = 0
world.print()
while not world.make_move(pi) and i < 10:
    print('\n=============================\n')
    world.print()
    i += 1

print('\n=============================\n')
