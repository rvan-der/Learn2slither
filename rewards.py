from enums import Status as St


class RewardStructure:

    def __init__(self, alive=0, dead=-5, green=2, red=-2,
                 target_len=10, penalty=-1):
        self.target_len = target_len
        self.penalty = penalty
        self.rewards = {
            St.ALIVE: alive,
            St.DEAD: dead,
            St.GREEN: green,
            St.RED: red
        }
        self.validate()

    def set_rewards(self, alive, dead, green, red):
        self.rewards = {
            St.ALIVE: alive,
            St.DEAD: dead,
            St.GREEN: green,
            St.RED: red
        }
        self.validate()

    def validate(self):
        err_msg = """Reward structure must follow these constraints:
   0 <= alive <= 100
-100 <= dead  <  0
   0 <  green <= 100
-100 <= red   <  0
   0 <= target length <= 100
-100 <= penalty       <= 0"""
        if self.rewards['alive'] < 0 or self.rewards['alive'] > 100:
            raise ValueError(err_msg)
        if self.rewards['dead'] < -100 or self.rewards['dead'] >= 0:
            raise ValueError(err_msg)
        if self.rewards['green'] <= 0 or self.rewards['green'] > 100:
            raise ValueError(err_msg)
        if self.rewards['red'] < -100 or self.rewards['red'] >= 0:
            raise ValueError(err_msg)
        if self.target_len < 0 or self.target_len > 100:
            raise ValueError(err_msg)
        if self.penalty < -100 or self.penalty > 0:
            raise ValueError(err_msg)

    def set_target_len(self, target_len):
        self.target_len = target_len
        self.validate()

    def set_penalty(self, penalty):
        self.penalty = penalty
        self.validate()

    def get(self, status, length):
        reward = self.rewards[status]
        if length < self.target_len and status != St.GREEN:
            reward += self.penalty
        return reward
