from os.path import join
from os import listdir, remove
from shutil import copyfile

from GridWorld import GridWorld
from QLearning import QLearning

def welcome_message() -> None:
    with open(join('assets', 'welcome_message.txt'), 'r') as f:
        print(f.read())
    print()

def play_level(level: int, agent: QLearning) -> bool:
    level_path = join('assets', f'level_{level}.txt')
    print(f'You are trying to beat level: {level_path}')
    
    for i in range(3):
        training_level_name = f'training_level_{level*3+i}.txt'
        copyfile(join('assets','edit_level.txt'), training_level_name)

        print(f'Please edit: {training_level_name}')
        input('Press enter when you\'re done.')
        print()

    print('Nice job! Now, I\'m going to train the agent on these levels and we\'ll give it a try!')
    for i in range(3):
        training_level_name = f'training_level_{level*3+i}.txt'
        env = GridWorld.from_file(training_level_name)
        agent.env = env

        print(f'Training on {training_level_name}...')
        agent.train(1_000)

    agent.env = GridWorld.from_file(level_path)
    agent_won = agent.visualize_policy_playthrough()

    return agent_won

def main():
    welcome_message()
    agent = QLearning(None)
    player_lost = False

    for lvl in range(5):
        player_successful = play_level(lvl, agent)

        if not player_successful:
            print('Your agent couldn\'t win. Therefore, you lose!!!')
            player_lost = True
            break

    if not player_lost:
        print('Wow, you did a really good job! Now, let me show you a level that your agent can\'t beat!')
        env = GridWorld(10,10)
        env.random_grid()
        agent.env = env
        agent_won = agent.visualize_policy_playthrough()

        if agent_won:
            print('Wow, you managed to win! That\'s crazy!')
        else:
            print('See!? I told you, your agent lost!')


    print('I\'ve deleted you training files so you can\'t cheat!')
    for file_name in listdir('.'):
        if 'training_level' in file_name:
            remove(file_name)

if __name__ == '__main__':
    main()