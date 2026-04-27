import random
import json
import os
from qtable import QTable
from enums import Direction as Dr, Tile as Tl
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

    def new(self, td_n=1, epsilon=0.5, alpha=0.1, gamma=0.9, rewards=None,
            name=None, color=None, filepath=None):
        agent = Agent()
        agent.set_file_path(filepath)
        agent.set_learning_params(td_n, epsilon, alpha, gamma)
        if rewards is not None:
            agent.set_rewards(rewards)
        agent.set_name(self.random_name() if name is None else name)
        agent.set_color(self.random_color() if color is None else color)
        return agent

    def validate_file(self, data):
        keys = {'td_n', 'epsilon', 'alpha', 'gamma', 'qtable', 'rewards',
                'name', 'sessions', 'color'}
        if not isinstance(data, dict) or set(data.keys()) != keys:
            raise ValueError("Wrong data type.")

        if not isinstance(data['td_n'], int) \
                or data['td_n'] < 0:
            raise ValueError("Wrong value for td_n.")

        if not isinstance(data['epsilon'], float) \
                and not isinstance(data['epsilon'], int) \
                or data['epsilon'] < 0 \
                or data['epsilon'] > 1:
            raise ValueError("Wrong value for epsilon.")

        if not isinstance(data['alpha'], float) \
                and not isinstance(data['alpha'], int) \
                or data['alpha'] < 0 \
                or data['alpha'] > 1:
            raise ValueError("Wrong value for alpha.")

        if not isinstance(data['gamma'], float) \
                and not isinstance(data['gammma'], int) \
                or data['gamma'] < 0 \
                or data['gamma'] > 1:
            raise ValueError("Wrong value for gamma.")

        if not isinstance(data['name'], str):
            raise ValueError("Wrong data type for name.")
        if len(data['name'] > 15):
            raise ValueError("Name too long.")

        if not isinstance(data['sessions'], int) \
                or data['sessions'] < 0:
            raise ValueError("Wrong value for number of sessions")

        if not isinstance(data['color'], list) \
                or len(data['color']) != 3:
            raise ValueError("Wrong data type for color.")
        for c in data['color']:
            if not isinstance(c, int) or c < 0 or c > 255:
                raise ValueError("Wrong value in color.")

        keys = {'rewards', 'target_len', 'penalty'}
        if not isinstance(data['rewards'], dict) \
                or set(data['rewards'].keys()) != keys:
            raise ValueError("Wrong data type for reward structure.")

        if not isinstance(data['rewards']['target_len'], int) \
                or data['rewards']['target_len'] < 0 \
                or data['rewards']['target_len'] > 100:
            raise ValueError("Wrong value for target length.")

        if not isinstance(data['rewards']['penalty'], int) \
                or data['rewards']['penalty'] < -100 \
                or data['rewards']['penalty'] > 0:
            raise ValueError("Wrong value for penalty.")

        keys = {'alive', 'dead', 'green', 'red'}
        if not isinstance(data['rewards']['rewards'], dict) \
                or set(data['rewards']['rewards'].keys()) != keys:
            raise ValueError("Wrong data type for reward values.")
        for v in data['rewards']['rewards'].values():
            if not isinstance(v, int) and not isinstance(v, float):
                raise ValueError("Wrong data type for reward values.")
        if data['rewards']['rewards']['alive'] < 0 \
                or data['rewards']['rewards']['alive'] > 100:
            raise ValueError("Wrong value for alive reward.")
        if data['rewards']['rewards']['dead'] < -100 \
                or data['rewards']['rewards']['dead'] >= 0:
            raise ValueError("Wrong value for dead reward.")
        if data['rewards']['rewards']['green'] <= 0 \
                or data['rewards']['rewards']['green'] > 100:
            raise ValueError("Wrong value for green reward.")
        if data['rewards']['rewards']['red'] < -100 \
                or data['rewards']['rewards']['red'] >= 0:
            raise ValueError("Wrong value for red reward.")

        if not isinstance(data['qtable'], dict):
            raise ValueError("Wrong data type for qtable.")
        for state, actions in data['qtable']:
            if not isinstance(state, str) or len(state) != 24:
                raise ValueError(
                    "Wrong data type for state key inside qtable."
                )
            for c in state:
                if c not in "0WHSRG":
                    raise ValueError("Wrong state key format inside qtable.")
            if not isinstance(actions, list) or len(actions) != 4:
                raise ValueError("Wrong data type for actions inside qtable.")
            for a in actions:
                if not isinstance(a, int) and not isinstance(a, float):
                    raise ValueError(
                        "Wrong data type for actions inside qtable."
                    )

    def from_file(self, filepath):
        if not filepath.endswith(".l2s"):
            raise NotAnAgentFile("Wrong file extension.")
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.validate_file(data)
            agent = Agent()
            agent.set_file_path(filepath)
            agent.rewards.set_target_len(data['rewards']['target_len'])
            agent.rewards.set_penalty(data['rewards']['penalty'])
            agent.rewards.set_rewards(
                data['rewards']['rewards']['alive'],
                data['rewards']['rewards']['dead'],
                data['rewards']['rewards']['green'],
                data['rewards']['rewards']['red']
            )
            agent.set_learning_params(
                data['td_n'],
                data['epsilon'],
                data['alpha'],
                data['gamma']
            )
            agent.qtable.set_table(data['qtable']['qtable'])
            agent.set_name(data['name'])
            agent.set_color(data['color'])
            agent.sessions = data['sessions']
            return agent

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
        vowels = 'aaaaeeeeiiiioooouuy'
        consonants = 'bbccddfffgghhhjkllmmnnppqrrsssssstvwxzzzz'
        parity = random.randint(0, 1)
        _len = random.randint(3, 5)

        name = ""
        for i in range(_len):
            if i % 2 == parity:
                name += random.choice(list(consonants))
                if random.random() < 0.05:
                    name += random.choice(list(consonants))
            else:
                name += random.choice(list(vowels))
                if random.random() < 0.1:
                    name += random.choice(list(vowels))

        return name.title() + str(random.randint(0, 999))


class Agent:

    def __init__(self):
        # td_n: temporal difference degree
        # epsilon: exploration rate
        # alpha: learning rate
        # gamma: discount factor
        self.filepath = None
        self.td_n = 0
        self.epsilon = 0
        self.alpha = 0
        self.gamma = 0
        self.qtable = QTable()
        self.rewards = RewardStructure()
        self.name = "Noname"
        self.sessions = 0
        self.color = [0, 0, 0]

    def set_file_path(self, filepath):
        if filepath is None or filepath == "":
            self.filepath = None
            return
        basename = os.path.basename(filepath)
        if basename is None or basename == "":
            raise ValueError("No filename provided.")
        if basename[0] == '.':
            raise ValueError("The file's name can't start with '.'")
        if not basename.endswith(".l2s"):
            raise ValueError("The file must have the .l2s extension.")
        if '/' not in filepath:
            filepath = f"./{filepath}"
        self.filepath = filepath

    def set_learning_params(self, td_n, epsilon, alpha, gamma):
        self.td_n = td_n
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def set_rewards(self, rewards):
        self.rewards = rewards

    def set_name(self, name):
        self.name = name

    def set_color(self, color):
        self.color = color

    def choose_action(self, state, training=True):
        if training and random.random() < self.epsilon:
            return self.random_action(state)
        return self.qtable.get_best_action(state)

    def random_action(self, state):
        options = list(Dr)
        x, y = state.headX, state.headY
        while len(options) > 0:
            action = random.choice(options)
            if action == Dr.UP and state.col[y - 1] in (Tl.WALL, Tl.BODY):
                options.remove(action)
            elif action == Dr.DOWN and state.col[y + 1] in (Tl.WALL, Tl.BODY):
                options.remove(action)
            elif action == Dr.LEFT and state.row[x - 1] in (Tl.WALL, Tl.BODY):
                options.remove(action)
            elif action == Dr.RIGHT and state.row[x + 1] in (Tl.WALL, Tl.BODY):
                options.remove(action)
            else:
                return action
        return random.choice(list(Dr))

    def save_to_file(self):
        path = ""
        if self.filepath is None:
            path = AgentFactory.default_filepath(self.name)
        else:
            path = os.path.expanduser(self.filepath)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as f:
            json.dump(
                self,
                f,
                default=lambda o: o.__dict__,
                separators=(',', ':')
            )


if __name__ == "__main__":
    factory = AgentFactory()
    agent = factory.new(3, RewardStructure(), 0.5, 0.1, 0.9)
    # agent.qtable.init_state("state1")
    # agent.qtable.init_state("state2")
    # agent.qtable.init_state("state3")
    agent.save_to_file()
