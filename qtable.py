class QTable:
    # Each state has 5 fields: the scores of the 4 actions and a counter
    # for the number of updates in the state (for temperature scheduling).

    def __init__(self):
        self.table = {}

    def set_table(self, table):
        self.table = table

    def get_state_values(self, state):
        qValues = self.table.get(state.key, None)
        if qValues is None:
            self.table[state.key] = [0] * 5
            return self.table[state.key]
        return qValues

    def get_qvalues(self, state):
        return self.get_state_values(state)[:4]

    def get_qvalue(self, state, action):
        qValues = self.get_state_values(state)
        return qValues[action]

    def set_qvalue(self, state, action, value):
        qValues = self.get_state_values(state)
        qValues[action] = value
        # Increment the updates counter.
        # Cap at 7000 to avoid math.exp overflow in softmax function
        qValues[4] = min(qValues[4] + 1, 7000)
