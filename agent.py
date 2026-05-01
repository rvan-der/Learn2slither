import random
import json
import os
from qtable import QTable
from enums import Status as St
from rewards import RewardStructure


class NotAnAgentFile(Exception):
    def __init__(self, message):
        super().__init__(message)


class AgentFactory:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(AgentFactory, cls).__new__(cls)
        return cls.instance

    def new(self, td_n=2, epsilon=0.5, alpha=0.1, gamma=0.9, rewards=None,
            name=None, color=None, filepath=None):
        agent = Agent()
        agent.set_learning_params(td_n, epsilon, alpha, gamma)
        if rewards is not None:
            agent.set_reward_struct(rewards)
        agent.set_name(self.random_name() if name is None else name)
        agent.set_color(self.random_color() if color is None else color)
        agent.save_to_file(filepath)
        return agent

    def data_from_file(self, filepath):
        filepath = os.path.expanduser(filepath)
        if not filepath.endswith(".l2s"):
            raise NotAnAgentFile("Wrong file extension.")
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.validate_file(data)
            return data

    def info_from_file(self, filepath):
        info = self.data_from_file(filepath)
        info.pop('qtable')
        return info

    def agent_from_data(self, data):
        agent = Agent()
        agent.rewardStruct.set_target_len(data['target_len'])
        agent.rewardStruct.set_penalty(data['penalty'])
        agent.rewardStruct.set_rewards(
            data['alive'],
            data['dead'],
            data['green'],
            data['red']
        )
        agent.set_learning_params(
            data['td_n'],
            data['epsilon'],
            data['alpha'],
            data['gamma']
        )
        agent.qtable.set_table(data['qtable'])
        agent.qtable.set_rewards(agent.rewardStruct.rewards)
        agent.set_name(data['name'])
        agent.set_color(data['color'])
        agent.sessions = data['sessions']
        return agent

    def agent_from_file(self, filepath):
        return self.agent_from_data(self.data_from_file(filepath))

    @staticmethod
    def default_filepath(name):
        dir = "/sgoinfre/goinfre/Perso/rvan-der"
        if not os.path.exists(dir):
            dir = os.path.expanduser("~/.local")
        path = f"{dir}/Learn2Slither/agents/{name}.l2s"
        i = 1
        while os.path.exists(path):
            path = f"{dir}/Learn2Slither/agents/{name}({i}).l2s"
            i += 1
        return path

    @staticmethod
    def random_color():
        color = [random.randint(0, 255) for _ in range(3)]
        if sum(color) < 100:
            color = [c * 1.2 for c in color]
        return color

    @staticmethod
    def random_name():
        vowels = 'aaaaeeeeiiiiiioooouuy'
        consonants = 'bbccddfffgghhhjkllmmnnppqrrsssssstvwxzzzz'
        parity = random.randint(0, 1)
        length = random.randint(3, 5)

        name = ""
        for i in range(length):
            if i % 2 == parity:
                name += random.choice(list(consonants))
                if random.random() < 0.05:
                    name += random.choice(list(consonants))
            else:
                name += random.choice(list(vowels))
                if random.random() < 0.1:
                    name += random.choice(list(vowels))

        return name.title() + str(random.randint(1, 999))

    def validate_file(self, data):
        keys = {'name', 'color', 'td_n', 'alpha', 'epsilon', 'gamma',
                'alive', 'dead', 'green', 'red', 'target_len',
                'penalty', 'sessions', 'qtable'}
        if not isinstance(data, dict) or set(data.keys()) != keys:
            raise ValueError("Wrong data type.")

        if not isinstance(data['name'], str):
            raise ValueError("Wrong data type for name.")
        if len(data['name']) > 20:
            raise ValueError("Name too long.")

        if not isinstance(data['color'], list) \
                or len(data['color']) != 3:
            raise ValueError("Wrong data type for color.")
        for c in data['color']:
            if not isinstance(c, int) or c < 0 or c > 255:
                raise ValueError("Wrong value in color.")

        if not isinstance(data['td_n'], int) \
                or data['td_n'] < 0:
            raise ValueError("Wrong value for td_n.")

        if not isinstance(data['alpha'], float) \
                and not isinstance(data['alpha'], int) \
                or data['alpha'] < 0 \
                or data['alpha'] > 1:
            raise ValueError("Wrong value for alpha.")

        if not isinstance(data['epsilon'], float) \
                and not isinstance(data['epsilon'], int) \
                or data['epsilon'] < 0 \
                or data['epsilon'] > 1:
            raise ValueError("Wrong value for epsilon.")

        if not isinstance(data['gamma'], float) \
                and not isinstance(data['gamma'], int) \
                or data['gamma'] < 0 \
                or data['gamma'] > 1:
            raise ValueError("Wrong value for gamma.")

        if not isinstance(data['alive'], float) \
                and not isinstance(data['alive'], int) \
                or data['alive'] < 0 or data['alive'] > 100:
            raise ValueError("Wrong value for alive reward.")

        if not isinstance(data['dead'], float) \
                and not isinstance(data['dead'], int) \
                or data['dead'] < -100 or data['dead'] >= 0:
            raise ValueError("Wrong value for dead reward.")

        if not isinstance(data['green'], float) \
                and not isinstance(data['green'], int) \
                or data['green'] <= 0 or data['green'] > 100:
            raise ValueError("Wrong value for green reward.")

        if not isinstance(data['red'], float) \
                and not isinstance(data['red'], int) \
                or data['red'] < -100 or data['red'] >= 0:
            raise ValueError("Wrong value for red reward.")

        if not isinstance(data['target_len'], int) \
                or data['target_len'] < 0 \
                or data['target_len'] > 100:
            raise ValueError("Wrong value for target length.")

        if not isinstance(data['penalty'], float) \
                and not isinstance(data['penalty'], int) \
                or data['penalty'] < -100 \
                or data['penalty'] > 0:
            raise ValueError("Wrong value for penalty.")

        if not isinstance(data['sessions'], int) \
                or data['sessions'] < 0:
            raise ValueError("Wrong value for number of sessions")

        if not isinstance(data['qtable'], dict):
            raise ValueError("Wrong data type for qtable.")
        for state, actions in data['qtable'].items():
            if not isinstance(state, str):
                raise ValueError(
                    "Wrong data type for state key inside qtable."
                )
            if len(state) > 5 or not all(c in "0123456789" for c in state):
                raise ValueError("Wrong state key format inside qtable.")
            if not isinstance(actions, list) or len(actions) != 4:
                raise ValueError("Wrong data type for actions inside qtable.")
            if not all(isinstance(a, int) or isinstance(a, float)
                       for a in actions):
                raise ValueError("Wrong data type for actions inside qtable.")


class Agent():

    def __init__(self):
        super().__init__()
        # td_n: temporal difference degree
        # epsilon: exploration rate
        # alpha: learning rate
        # gamma: discount factor
        self.td_n = 1
        self.epsilon = 0.5
        self.alpha = 0.1
        self.gamma = 0.9
        self.qtable = QTable()
        self.rewardStruct = RewardStructure()
        self.name = "Noname"
        self.sessions = 0
        self.color = [0, 0, 0]

    def set_learning_params(self, td_n, epsilon, alpha, gamma):
        self.td_n = td_n
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def set_reward_struct(self, rewardStruct):
        self.rewardStruct = rewardStruct
        self.qtable.set_rewards(rewardStruct.rewards)

    def set_name(self, name):
        self.name = name

    def set_color(self, color):
        self.color = color

    def increment_sessions(self):
        self.sessions += 1

    def choose_action(self, state, training=True):
        if training and random.random() < self.epsilon:
            return self.qtable.random_action(state)
        return self.qtable.best_action(state)

    def get_info(self):
        return {
            'name': self.name,
            'color': self.color,
            'td_n': self.td_n,
            'alpha': self.alpha,
            'epsilon': self.epsilon,
            'gamma': self.gamma,
            'alive': self.rewardStruct.rewards[St.ALIVE],
            'dead': self.rewardStruct.rewards[St.DEAD],
            'green': self.rewardStruct.rewards[St.GREEN],
            'red': self.rewardStruct.rewards[St.RED],
            'target_len': self.rewardStruct.target_len,
            'penalty': self.rewardStruct.penalty,
            'sessions': self.sessions
        }

    def get_data(self):
        data = self.get_info()
        data['qtable'] = self.qtable.table
        return data

    def save_to_file(self, filepath=None):
        if filepath is None or filepath == "":
            filepath = AgentFactory.default_filepath(self.name)

        filepath = os.path.expanduser(filepath)
        dirname, basename = os.path.split(filepath)

        if basename is None or basename == "":
            raise ValueError("No filename provided.")
        if basename[0] == '.':
            raise ValueError("The file's name can't start with '.'")
        if not basename.endswith(".l2s"):
            raise ValueError("The file must have the .l2s extension.")

        if '/' not in filepath:
            filepath = f"./{filepath}"
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        data = self.get_data()
        with open(filepath, 'w') as f:
            json.dump(data, f, separators=(',', ':'))


if __name__ == "__main__":
    factory = AgentFactory()
    agent = factory.new(3, RewardStructure(), 0.5, 0.1, 0.9)
    # agent.qtable.init_state("state1")
    # agent.qtable.init_state("state2")
    # agent.qtable.init_state("state3")
    agent.save_to_file()
