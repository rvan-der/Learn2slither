import numpy as np
from collections import deque
from l2s_enums import Direction as Dr
from l2s_enums import Tile as Tl
from l2s_enums import Status as St


class State:

    def __init__(self, horizontal, vertical):
        self.hz = horizontal
        self.vt = vertical

    def __str__(self):
        s = ''
        width = self.hz.find(str(Tl.HEAD)) + 1
        for v in self.vt:
            if v == str(Tl.HEAD):
                s += self.hz + '\n'
            else:
                s += v.rjust(width) + '\n'
        return s[:-1]


class Environment:

    rng = np.random.default_rng()

    def __init__(self, rewards, rows=10, cols=10, initial_len=3):
        self.rewards = rewards
        self.rows = rows
        self.cols = cols
        self.initial_len = initial_len
        self.initialize_env()

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.board)

    def set_rewards(self, rewards):
        self.rewards = rewards

    def is_oob(self, position):  # oob = out of bounds
        row, col = position
        return row < 0 or row >= self.rows or col < 0 or col >= self.cols

    def move_coords(self, position, direction, steps=1):
        row, col = position
        if direction == Dr.UP:
            return (row - steps, col)
        if direction == Dr.DOWN:
            return (row + steps, col)
        if direction == Dr.LEFT:
            return (row, col - steps)
        if direction == Dr.RIGHT:
            return (row, col + steps)
        return position

    def initialize_env(self):
        # Initialize board, snake and status
        self.status = St.ALIVE
        self.board = np.full((self.rows, self.cols), str(Tl.EMPTY), dtype=str)
        self.snake = deque(maxlen=self.rows * self.cols + 1)
        # Choose a random starting position for the snake head
        pos = tuple(self.rng.choice([(y, x) for y in range(self.rows)
                                    for x in range(self.cols)]))
        # Build the snake
        self.snake.append(pos)
        self.board[pos] = str(Tl.HEAD)
        for _ in range(self.initial_len - 1):
            moved = ()
            directions = list(Dr)
            while True:
                dir = self.rng.choice(directions)
                moved = self.move_coords(pos, dir)
                if self.is_oob(moved) or self.board[moved] != str(Tl.EMPTY):
                    directions.remove(dir)
                else:
                    pos = moved
                    break
            self.snake.append(pos)
            self.board[pos] = str(Tl.BODY)
        # Place apples
        self.place_apple(str(Tl.GREEN))
        self.place_apple(str(Tl.GREEN))
        self.place_apple(str(Tl.RED))

    def place_apple(self, apple):
        pos = tuple(self.rng.choice([(y, x) for y in range(self.rows)
                                    for x in range(self.cols)
                                    if self.board[y, x] == str(Tl.EMPTY)]))
        self.board[pos] = apple

    def move_snake(self, direction):
        if self.status == St.DEAD:
            return
        old_head = self.snake[0]
        new_head = self.move_coords(old_head, direction)
        # Check for collisions
        if self.is_oob(new_head) or self.board[new_head] == str(Tl.BODY):
            self.status = St.DEAD
            return
        # Extend snake from the head
        tile = self.board[new_head]
        self.board[new_head] = str(Tl.HEAD)
        self.board[old_head] = str(Tl.BODY)
        self.snake.appendleft(new_head)
        # Handle green apple eaten
        if tile == str(Tl.GREEN):
            self.place_apple(str(Tl.GREEN))
            self.status = St.GREEN
            return
        # Handle normal movement (remove tail)
        self.board[self.snake.pop()] = str(Tl.EMPTY)
        # Handle red apple eaten
        if tile == str(Tl.RED):
            if len(self.snake) == 1:
                self.status = St.DEAD
                return
            self.board[self.snake.pop()] = str(Tl.EMPTY)
            self.place_apple(str(Tl.RED))
            self.status = St.RED
            return
        self.status = St.ALIVE

    def get_state(self):
        y, x = self.snake[0]
        hz = ''.join(self.board[y])
        vt = ''.join(self.board[i, x] for i in range(self.rows))
        return State(hz, vt)

    def get_reward(self):
        return self.rewards[self.status]


if __name__ == "__main__":
    rewards = {St.ALIVE: 0, St.DEAD: -2,
               St.GREEN: 1, St.RED: -1}
    env = Environment(rewards, 10, 10)
    print(env)
    print(env.status)
    print(env.get_state(), end='\n\n')
    while True:
        try:
            direction = Dr.from_str(input("direction: "))
        except ValueError:
            print("invalid direction")
            continue
        env.move_snake(direction)
        print(env)
        print(str(env.status))
        if env.status == St.DEAD:
            _continue = input("restart? (y/n): ").lower()
            if _continue == 'y' or _continue == 'yes':
                env.initialize_env()
                print(env)
                print(env.status)
                print(env.get_state(), end='\n\n')
            else:
                break
        else:
            print(env.get_state(), end='\n\n')
