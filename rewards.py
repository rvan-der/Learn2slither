from enums import Status as St


class RewardStructure:

    def __init__(self, alive=0, dead=-5, green=2, red=-2):
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
        err_msg = """Reward structure must follow these constraints
-100 <= alive <= 100
-100 <= dead  <  0
   0 <  green <= 100
-100 <= red   <  0"""
        if self.rewards['alive'] < -100 or self.rewards['alive'] > 100:
            raise ValueError(err_msg)
        if self.rewards['dead'] < -100 or self.rewards['dead'] >= 0:
            raise ValueError(err_msg)
        if self.rewards['green'] <= 0 or self.rewards['green'] > 100:
            raise ValueError(err_msg)
        if self.rewards['red'] < -100 or self.rewards['red'] >= 0:
            raise ValueError(err_msg)

    def get_from_status(self, status):
        return self.rewards[status]
