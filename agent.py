import random
import json
import os
import math
from qtable import QTable
from enums import Direction as Dr
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

    def new(self, td_n=2, alpha=0.1, gamma=0.9, kappa=0.01, epsilon=0.001,
            rewards=None, name=None, color=None, filepath=None):
        agent = Agent()
        agent.set_learning_params(td_n, alpha, gamma, kappa, epsilon)
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
        agent.rewardStruct.set_rewards(
            data['alive'],
            data['dead'],
            data['green'],
            data['red']
        )
        agent.set_learning_params(
            data['td_n'],
            data['alpha'],
            data['gamma'],
            data['kappa'],
            data['epsilon']
        )
        agent.qtable.set_table(data['qtable'])
        agent.set_name(data['name'])
        agent.set_color(data['color'])
        agent.sessions = data['sessions']
        return agent

    def agent_from_file(self, filepath):
        return self.agent_from_data(self.data_from_file(filepath))

    @staticmethod
    def default_folder():
        return os.path.expanduser("~/.local/Learn2Slither/agents")

    @staticmethod
    def default_filepath(name):
        folder = AgentFactory.default_folder()
        path = f"{folder}/{name}.l2s"
        i = 1
        while os.path.exists(path):
            path = f"{folder}/{name}({i}).l2s"
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
        keys = {'name', 'color', 'td_n', 'alpha', 'gamma', 'kappa', 'epsilon',
                'alive', 'dead', 'green', 'red', 'sessions', 'qtable'}
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
                or data['alpha'] <= 0 \
                or data['alpha'] > 1:
            raise ValueError("Wrong value for alpha.")

        if not isinstance(data['gamma'], float) \
                and not isinstance(data['gamma'], int) \
                or data['gamma'] <= 0 \
                or data['gamma'] > 1:
            raise ValueError("Wrong value for gamma.")

        if not isinstance(data['kappa'], float) \
                and not isinstance(data['kappa'], int) \
                or data['kappa'] <= 0 \
                or data['kappa'] > 1:
            raise ValueError("Wrong value for kappa.")

        if not isinstance(data['epsilon'], float) \
                and not isinstance(data['epsilon'], int) \
                or data['epsilon'] < 0 \
                or data['epsilon'] > 1:
            raise ValueError("Wrong value for epsilon.")

        if not isinstance(data['alive'], float) \
                and not isinstance(data['alive'], int) \
                or data['alive'] < -100 or data['alive'] > 100:
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
            if state != "DEAD" and\
                    (len(state) > 4
                        or not all(c in "0123456789" for c in state)
                        or int(state) > 4095):
                raise ValueError("Wrong state key format inside qtable.")
            if not isinstance(actions, list) or len(actions) != 5:
                raise ValueError("Wrong data type for actions inside qtable.")
            if not all(isinstance(a, int) or isinstance(a, float)
                       for a in actions):
                raise ValueError("Wrong data type for actions inside qtable.")


class Agent():

    def __init__(self):
        super().__init__()
        # td_n: temporal difference degree
        # alpha: learning rate
        # gamma: discount factor
        # kappa: temperature scheduling factor
        self.td_n = 0
        self.alpha = 0.1
        self.gamma = 0.9
        self.kappa = 0.01
        self.epsilon = 0.001
        self.qtable = QTable()
        self.rewardStruct = RewardStructure()
        self.name = "Noname"
        self.sessions = 0
        self.color = [0, 0, 0]

    def set_learning_params(self, td_n, alpha, gamma, kappa, epsilon):
        err_msg = """Learning parameters must follow these constraints:
       td_n   >= 0
1  >=  alpha  >  0
1  >=  gamma  >  0
1  >=  kappa  >  0
1  >= epsilon >= 0"""
        if td_n < 0:
            raise ValueError(err_msg)
        if alpha > 1 or alpha <= 0:
            raise ValueError(err_msg)
        if gamma > 1 or gamma <= 0:
            raise ValueError(err_msg)
        if kappa > 1 or kappa <= 0:
            raise ValueError(err_msg)
        if epsilon > 1 or epsilon < 0:
            raise ValueError(err_msg)
        self.td_n = td_n
        self.alpha = alpha
        self.gamma = gamma
        self.kappa = kappa
        self.epsilon = epsilon

    def set_reward_struct(self, rewardStruct):
        self.rewardStruct = rewardStruct

    def set_name(self, name):
        self.name = name

    def set_color(self, color):
        self.color = color

    def increment_sessions(self):
        self.sessions += 1

    def choose_action(self, state, training=True):
        if training:
            if random.random() < self.epsilon:
                return random.choice(list(Dr))
            return self.softmax_action(state)
        return self.best_action(state)

    def best_action(self, state):
        qValues = self.qtable.get_qvalues(state)
        max_q = max(qValues)
        tolerance = math.log(0.000001 + max_q - min(qValues))
        return random.choice(
            [a for a in Dr
             if qValues[a] == max_q or max_q - qValues[a] < tolerance]
        )

    def softmax_action(self, state):
        stateValues = self.qtable.get_state_values(state)

        qValues = stateValues[:4]
        # To avoid math.exp overflow
        scale = max(1, max([abs(q) for q in qValues]))
        qValues = [q / scale for q in qValues]

        visits = stateValues[4]
        beta = 0.00000001 + self.kappa * visits  # Inverse temperature
        # print(f'b: {beta}, "{state.key}": [{qValues[0]}, {qValues[1]}, {qValues[2]}, {qValues[3]}, {visits}]')

        expQValues = [math.exp(beta * q) for q in qValues]
        expSum = sum(expQValues)

        distribution = [expQ / expSum for expQ in expQValues]
        return random.choices(list(Dr), weights=distribution)[0]

    def random_action(self):
        return random.choice(list(Dr))

    def get_info(self):
        return {
            'name': self.name,
            'color': self.color,
            'td_n': self.td_n,
            'alpha': self.alpha,
            'gamma': self.gamma,
            'kappa': self.kappa,
            'epsilon': self.epsilon,
            'alive': self.rewardStruct.rewards[St.ALIVE],
            'dead': self.rewardStruct.rewards[St.DEAD],
            'green': self.rewardStruct.rewards[St.GREEN],
            'red': self.rewardStruct.rewards[St.RED],
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
