import numpy as np
from l2s_qtable import QTable
from l2s_enums import Direction as Dr


class Agent:

    rng = np.random.default_rng()

    def __init__(self, rewards, epsilon=0.5, alpha=0.1, gamma=0.9):
        # epsilon: exploration rate
        # alpha: learning rate
        # gamma: discount factor
        self.rewards = rewards
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.qtable = QTable()

    def choose_action(self, state, training=True):
        if training and self.rng.random() < self.epsilon:
            return self.rng.choice(Dr)
        return self.qtable.get_best_action(state)
