import random
import json
import os
from qtable import QTable
from enums import Direction as Dr, Tile as Tl
from rewards import RewardStructure


class AgentFactory:

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(AgentFactory, cls).__new__(cls)
        return cls.instance

    def new(self, td_n, rewards, epsilon=0.1, alpha=0.1, gamma=0.9):
        agent = Agent()
        agent.set_rewards(rewards)
        agent.set_learning_params(td_n, epsilon, alpha, gamma)
        agent.set_name(self.random_name())
        agent.set_color(self.random_color())
        return agent

    def from_file(self, filepath):
        if not filepath.endswith(".l2s"):
            raise 
        with open(filepath, 'r') as f:
            data = json.load(f)
            agent = Agent()
            agent.rewards.set_target_len(data['rewards']['target_len'])
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

    def random_color(self):
        color = [random.randint(0, 255) for _ in range(3)]
        if sum(color) < 100:
            color = [c * 1.2 for c in color]
        return color

    def random_name(self):
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
        self.td_n = 0
        self.epsilon = 0
        self.alpha = 0
        self.gamma = 0
        self.qtable = QTable()
        self.rewards = RewardStructure()
        self.name = "Noname"
        self.sessions = 0
        self.color = [0, 0, 0]

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

    def save_to_file(self, filename):
        filepath = '~/.l2s_agents/' + filename + '.l2s'
        filepath = os.path.expanduser(filepath)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'w') as f:
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
    agent.save_to_file("testagent.json")
