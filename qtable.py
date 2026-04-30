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
        self.table = {}

    def get_state_values(self, state):
        qvalues = self.table.get(state.key, None)
        if qvalues is None:
            self.init_state(state)
            qvalues = self.table[state.key]
        return qvalues

    def get_qvalue(self, state, action):
        qvalues = self.get_state_values(state)
        return qvalues[action]

    def set_qvalue(self, state, action, value):
        qvalues = self.get_state_values(state)
        qvalues[action] = value

    def best_action(self, state):
        qvalues = self.get_state_values(state)
        max_q = max(qvalues)
        return random.choice([a for a in Dr if qvalues[a] == max_q])

    def random_action(self, state):
        print("\n[RANDOM ACTION]")
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

    def init_state(self, state):
        # down = state.col[state.headY + 1]
        # up = state.col[state.headY - 1]
        # left = state.row[state.headX - 1]
        # right = state.row[state.headX + 1]
        self.table[state.key] = [0] * 4
        # self.table[state.key][Dr.DOWN] = self.tileValues[down]
        # self.table[state.key][Dr.UP] = self.tileValues[up]
        # self.table[state.key][Dr.LEFT] = self.tileValues[left]
        # self.table[state.key][Dr.RIGHT] = self.tileValues[right]

    def set_table(self, table):
        self.table = table
