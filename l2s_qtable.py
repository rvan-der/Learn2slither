import numpy as np
from l2s_enums import Direction as Dr


class QTable:

    rng = np.random.default_rng()

    def __init__(self):
        self.qtable = {}

    def get_state_values(self, state):
        qvalues = self.qtable.get(state.key, None)
        if qvalues is None:
            self.init_state(state.key)
            qvalues = self.qtable[state.key]
        return qvalues

    def get_qvalue(self, state, action):
        qvalues = self.get_state_values(state)
        return qvalues[action]

    def set_qvalue(self, state, action, value):
        qvalues = self.get_state_values(state)
        qvalues[action] = value

    def get_best_action(self, state):
        qvalues = self.get_state_values(state)
        max_q = max(qvalues)
        return self.rng.choice([a for a in Dr if qvalues[a] == max_q])

    def init_state(self, key):
        self.qtable[key] = [0.0 for _ in Dr]
