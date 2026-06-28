class QTable:

    def __init__(self):
        self.table = {}

    def set_table(self, table):
        self.table = table

    def get_state_values(self, state):
        qValues = self.table.get(state.key, None)
        if qValues is None:
            self.table[state.key] = [0] * 4
            return self.table[state.key]
        return qValues

    def get_qvalue(self, state, action):
        qValues = self.get_state_values(state)
        return qValues[action]

    def set_qvalue(self, state, action, value):
        qValues = self.get_state_values(state)
        qValues[action] = value
