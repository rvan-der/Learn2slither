from enums import Status as St
import math


class RewardStructure:

    def __init__(self, alive=0.0, dead=-5.0, green=1.0, red=-1.0,
                 target_len=math.inf):
        if dead >= 0 or green <= 0 or red > 0:
            raise ValueError("Reward values must follow these constraints:\n" +
                             "dead < 0, green > 0, red <= 0")
        self.target_len = target_len
        self.rewards = {
            St.ALIVE: alive,
            St.DEAD: dead,
            St.GREEN: green,
            St.RED: red
        }

    def set_rewards(self, alive, dead, green, red):
        if dead >= 0 or green <= 0 or red > 0:
            raise ValueError("Reward values must follow these constraints:\n" +
                             "dead < 0, green > 0, red <= 0")
        self.rewards = {
            St.ALIVE: alive,
            St.DEAD: dead,
            St.GREEN: green,
            St.RED: red
        }

    def set_target_len(self, target_len):
        self.target_len = target_len

    def get(self, status, length):
        base_rwd = self.rewards[status]
        if length >= self.target_len:
            if status == St.ALIVE:
                return base_rwd * (1.5 if base_rwd > 0 else 0.5)
            if status == St.RED:
                return base_rwd * 0.5
        return base_rwd
