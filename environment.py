import random
from collections import deque
from enums import Direction as Dr
from enums import Tile as Tl
from enums import Status as St
from rewards import RewardStructure
from PySide6.QtCore import (QObject, Signal)


class State:

    def __init__(self, row, col, status):
        self.row = row
        self.col = col
        self.status = status
        self.headX = row.find(Tl.HEAD)
        self.headY = col.find(Tl.HEAD)
        self.key = self.row + self.col

    def __str__(self):
        s = ''
        width = self.headX + 1
        for v in self.col:
            if v == Tl.HEAD:
                s += self.row + '\n'
            else:
                s += v.rjust(width) + '\n'
        return s[:-1]


class Environment(QObject):

    cellUpdate = Signal(int, int, Tl)
    sizeChanged = Signal()

    def __init__(self, height=10, width=10, initial_len=3, parent=None):
        if initial_len >= (height * width) // 4:
            raise ValueError(
                "Initial length must be less than a quarter of the board size."
                )
        if initial_len < 2:
            raise ValueError("Initial length must be at least 2.")
        if height < 10 or width < 10:
            raise ValueError("Height and width must be at least 10.")
        super().__init__(parent)
        self.height = height
        self.width = width
        self.initial_len = initial_len
        self.board = []
        self.snake = None
        self.status = None

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.board)

    def set_size(self, height, width):
        if height < 10 or width < 10:
            raise ValueError("Height and width must be at least 10.")
        self.sizeChanged.emit()
        self.height = height
        self.width = width
        self.init_env()

    def is_oob(self, position):  # oob = out of bounds
        x, y = position
        return y < 1 or y > self.height or x < 1 or x > self.width

    def move_coords(self, position, direction, steps=1):
        x, y = position
        if direction == Dr.UP:
            return (x, y - steps)
        if direction == Dr.DOWN:
            return (x, y + steps)
        if direction == Dr.LEFT:
            return (x - steps, y)
        if direction == Dr.RIGHT:
            return (x + steps, y)
        return position

    def init_empty_board(self):
        self.status = None
        self.board = []
        self.board.append([Tl.WALL] * (self.width + 2))
        for _ in range(1, self.height + 1):
            self.board.append([Tl.WALL] + [Tl.EMPTY] * self.width + [Tl.WALL])
        self.board.append([Tl.WALL] * (self.width + 2))

        for y in range(self.height + 2):
            for x in range(self.width + 2):
                self.cellUpdate.emit(x, y, self.board[y][x])

    def new_game(self):
        self.init_empty_board()
        self.buildSnake()
        self.place_apple(Tl.GREEN)
        self.place_apple(Tl.GREEN)
        self.place_apple(Tl.RED)
        self.status = St.ALIVE

    def closest_wall(self, position):
        x, y = position
        closest = (Dr.UP, y)
        if self.height - y - 1 < closest[1]:
            closest = (Dr.DOWN, self.height - y - 1)
        if x < closest[1]:
            closest = (Dr.LEFT, x)
        if self.width - x - 1 < closest[1]:
            closest = (Dr.RIGHT, self.width - x - 1)
        return closest[0]

    def buildSnake(self):
        self.snake = deque(maxlen=self.height * self.width)
        success = False
        while not success:
            self.snake = deque(maxlen=self.height * self.width)
            pos = random.choice([(x, y) for y in range(1, self.height + 1)
                                for x in range(1, self.width + 1)])
            self.snake.append(pos)
            self.change_cell(pos, Tl.HEAD)
            closestWall = self.closest_wall(pos)
            success = True
            for _ in range(self.initial_len - 1):
                directions = list(Dr)
                directions.remove(closestWall)
                while len(directions) > 0:
                    dir = random.choice(directions)
                    moved = self.move_coords(pos, dir)
                    if self.is_oob(moved) \
                            or self.board[moved[1]][moved[0]] != Tl.EMPTY \
                            or moved in self.snake:
                        directions.remove(dir)
                    else:
                        pos = moved
                        break
                if len(directions) == 0:
                    success = False
                    self.init_empty_board()
                    break
                self.snake.append(pos)
                self.change_cell(pos, Tl.BODY)

    def place_apple(self, apple):
        pos = random.choice([(x, y) for y in range(self.height)
                            for x in range(self.width)
                            if self.board[y][x] == Tl.EMPTY])
        self.change_cell(pos, apple)

    def move_snake(self, direction):
        if self.status == St.DEAD:
            return
        old_head = self.snake[0]
        new_head = self.move_coords(old_head, direction)
        # Check for collisions
        if self.is_oob(new_head)\
                or self.board[new_head[1]][new_head[0]] == Tl.BODY:
            self.status = St.DEAD
            return
        # Extend snake from the head
        tile = self.board[new_head[1]][new_head[0]]
        self.change_cell(new_head, Tl.HEAD)
        self.change_cell(old_head, Tl.BODY)
        self.snake.appendleft(new_head)
        # Handle green apple eaten
        if tile == Tl.GREEN:
            self.place_apple(Tl.GREEN)
            self.status = St.GREEN
            return
        # Handle normal movement (remove tail)
        self.change_cell(self.snake.pop(), Tl.EMPTY)
        # Handle red apple eaten
        if tile == Tl.RED:
            if len(self.snake) == 1:
                self.status = St.DEAD
                return
            self.change_cell(self.snake.pop(), Tl.EMPTY)
            self.place_apple(Tl.RED)
            self.status = St.RED
            return
        self.status = St.ALIVE

    def change_cell(self, position, tile):
        self.board[position[1]][position[0]] = tile
        self.cellUpdate.emit(position[0], position[1], tile)

    def get_state(self):
        x, y = self.snake[0]
        row = ''.join(self.board[y])
        col = ''.join(self.board[i][x] for i in range(self.height + 2))
        return State(row, col, self.status)

    def get_reward(self, reward_struct):
        return reward_struct.get(self.status, len(self.snake))


if __name__ == "__main__":
    rewards = RewardStructure(target_len=10, alive=0.1)
    env = Environment(10, 10)
    env.new_game()
    print(env)
    print(str(env.status) + ' (' + str(env.get_reward(rewards)) + ')')
    print(env.get_state(), end='\n\n')
    while True:
        try:
            direction = Dr.from_str(input("direction: "))
        except ValueError:
            print("invalid direction")
            continue
        env.move_snake(direction)
        print(env)
        print(str(env.status) + ' (' + str(env.get_reward(rewards)) + ')')
        if env.status == St.DEAD:
            _continue = input("restart? (y/n): ").lower()
            if _continue == 'y' or _continue == 'yes':
                env.init_env()
                print(env)
                print(env.status + ' (' + str(env.get_reward(rewards)) + ')')
                print(env.get_state(), end='\n\n')
            else:
                break
        else:
            print(env.get_state(), end='\n\n')
