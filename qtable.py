import random
from enums import Direction as Dr
from enums import Tile as Tl


class QTable:

    tileValues = {
            Tl.WALL: -5,
            Tl.EMPTY: 0,
            Tl.BODY: -5,
            Tl.GREEN: 1,
            Tl.RED: -1
            }

    def __init__(self):
        self.qtable = {}

    def get_state_values(self, state):
        qvalues = self.qtable.get(state.key, None)
        if qvalues is None:
            self.init_state(state)
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
        return random.choice([a for a in Dr if qvalues[a] == max_q])

    def init_state(self, state):
        headX = state.row.find(Tl.HEAD)
        headY = state.col.find(Tl.HEAD)
        down = state.col[headY + 1]
        up = state.col[headY - 1]
        left = state.row[headX - 1]
        right = state.row[headX + 1]
        self.qtable[state.key] = [0] * len(Dr)
        self.qtable[state.key][Dr.DOWN] = self.tileValues[down]
        self.qtable[state.key][Dr.UP] = self.tileValues[up]
        self.qtable[state.key][Dr.LEFT] = self.tileValues[left]
        self.qtable[state.key][Dr.RIGHT] = self.tileValues[right]

    def set_table(self, qtable):
        self.qtable = qtable
