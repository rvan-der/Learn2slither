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
        # a scaled value of the space between the head and the view
        self.space = {}
        # the first non empty tile ahead in each direction
        self.view = {
            Dr.LEFT: self.left_view(),
            Dr.RIGHT: self.right_view(),
            Dr.UP: self.up_view(),
            Dr.DOWN: self.down_view()
        }
        self.key = self.encode()

    # This encoding serves to reduce and compress the information of states.
    # It significantly reduces the number of possible states while providing
    # useful information for a state initialization strategy in the Q-Table.
    # Keys in json format must be strings but even if we used only 1 character
    # per field, every key would be 8 chars long. By encoding each field
    # on a few bits, or-ing them into a number and then converting that
    # number into a string we can save a significant number of characters in
    # the models' file.
    # key code:
    # viewL | viewR | viewU | viewD | spaceL | spaceR | spaceU | spaceD
    # Every field is 2 bits wide (4 possible values).
    # total: 8 * 2 = 16 bits (65535 or 5 chars at most)
    def encode(self):
        viewCodes = {
            Tl.WALL: 0,
            Tl.BODY: 1,
            Tl.RED: 2,
            Tl.GREEN: 3
        }
        key = viewCodes[self.view[Dr.LEFT]] << 14
        key |= viewCodes[self.view[Dr.RIGHT]] << 12
        key |= viewCodes[self.view[Dr.UP]] << 10
        key |= viewCodes[self.view[Dr.DOWN]] << 8
        key |= self.space[Dr.LEFT] << 6
        key |= self.space[Dr.RIGHT] << 4
        key |= self.space[Dr.UP] << 2
        key |= self.space[Dr.DOWN]
        return str(key)

    def space_scaler(self, space):
        if space == 0:
            return 0
        if space < 4:
            return 1
        if space < 7:
            return 2
        return 3

    def left_view(self):
        i = 1
        while self.row[self.headX - i] == Tl.EMPTY:
            i += 1
        self.space[Dr.LEFT] = self.space_scaler(i - 1)
        return self.row[self.headX - i]
    
    def right_view(self):
        i = 1
        while self.row[self.headX + i] == Tl.EMPTY:
            i += 1
        self.space[Dr.RIGHT] = self.space_scaler(i - 1)
        return self.row[self.headX + i]

    def up_view(self):
        i = 1
        while self.col[self.headY - i] == Tl.EMPTY:
            i += 1
        self.space[Dr.UP] = self.space_scaler(i - 1)
        return self.col[self.headY - i]
    
    def down_view(self):
        i = 1
        while self.col[self.headY + i] == Tl.EMPTY:
            i += 1
        self.space[Dr.DOWN] = self.space_scaler(i - 1)
        return self.col[self.headY + i]

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

    def __init__(self, initial_len=3, displayOn=False, parent=None):
        if initial_len >= 25:
            raise ValueError(
                "Initial length must be less or equal to 25."
            )
        if initial_len < 2:
            raise ValueError("Initial length must be at least 2.")
        super().__init__(parent)
        self.displayOn = displayOn
        self.initial_len = initial_len
        self.board = []
        self.snake = None
        self.status = None

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.board)

    def is_oob(self, position):  # oob = out of bounds
        x, y = position
        return y < 1 or y > 10 or x < 1 or x > 10

    def move_coords(self, position, direction):
        x, y = position
        if direction == Dr.UP:
            return (x, y - 1)
        if direction == Dr.DOWN:
            return (x, y + 1)
        if direction == Dr.LEFT:
            return (x - 1, y)
        if direction == Dr.RIGHT:
            return (x + 1, y)
        return position

    def init_empty_board(self):
        self.status = None
        self.board = []
        self.board.append([Tl.WALL] * 12)
        for _ in range(1, 11):
            self.board.append([Tl.WALL] + [Tl.EMPTY] * 10 + [Tl.WALL])
        self.board.append([Tl.WALL] * 12)

        if self.displayOn:
            for y in range(12):
                for x in range(12):
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
        if 9 - y < closest[1]:
            closest = (Dr.DOWN, 9 - y)
        if x < closest[1]:
            closest = (Dr.LEFT, x)
        if 9 - x < closest[1]:
            closest = (Dr.RIGHT, 9 - x)
        return closest[0]

    def buildSnake(self):
        self.snake = deque(maxlen=100)
        success = False
        while not success:
            success = True
            self.snake = deque(maxlen=100)
            pos = random.choice([(x, y) for y in range(1, 11)
                                for x in range(1, 11)])
            self.snake.append(pos)
            self.change_cell(pos, Tl.HEAD)
            closestWall = self.closest_wall(pos)
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
        pos = random.choice([(x, y) for y in range(10)
                            for x in range(10)
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
        if self.displayOn:
            self.cellUpdate.emit(position[0], position[1], tile)

    def get_state(self):
        x, y = self.snake[0]
        row = ''.join(self.board[y])
        col = ''.join(self.board[i][x] for i in range(12))
        return State(row, col, self.status)

    def get_reward(self, reward_struct):
        return reward_struct.get(self.status, len(self.snake))


if __name__ == "__main__":
    rewards = RewardStructure(target_len=10, alive=0.1)
    env = Environment()
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
                env.new_game()
                print(env)
                print(env.status + ' (' + str(env.get_reward(rewards)) + ')')
                print(env.get_state(), end='\n\n')
            else:
                break
        else:
            print(env.get_state(), end='\n\n')
