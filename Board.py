import numpy as np
from collections import deque


class Board:

    rng = np.random.default_rng(42)

    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.board = np.full((rows, cols), '0', dtype=str)
        self.snake = deque()
        self.initialize_board()

    def is_oob(self, position):  # oob = out of bounds
        row, col = position
        return row < 0 or row >= self.rows or col < 0 or col >= self.cols

    def initialize_board(self):
        x = Board.rng.integers(0, self.rows)
        y = Board.rng.integers(0, self.cols)
        self.snake.append((x, y))
        self.board[x, y] = 'H'
        for _ in range(2):
            directions = ['up', 'down', 'left', 'right']
            dir = Board.rng.choice(directions)
            if dir == 'up':
                if self.is_oob((x, y - 1)) or self.board[x, y - 1] != '0':
                    directions.remove('up')
                    dir = Board.rng.choice(directions)
                else:
                    y -= 1
            if dir == 'down':
                if self.is_oob((x, y + 1)) or self.board[x, y + 1] != '0':
                    directions.remove('down')
                    dir = Board.rng.choice(directions)
                else:
                    y += 1
            if dir == 'left':
                if self.is_oob((x - 1, y)) or self.board[x - 1, y] != '0':
                    directions.remove('left')
                    dir = Board.rng.choice(directions)
                else:
                    x -= 1
            if dir == 'right':
                if self.is_oob((x + 1, y)) or self.board[x + 1, y] != '0':
                    directions.remove('right')
                    dir = Board.rng.choice(directions)
                else:
                    x += 1
            self.snake.append((x, y))
            self.board[x, y] = 'S'
            self.place_apple('green')
            self.place_apple('green')
            self.place_apple('red')

    def place_apple(self, color):
        pos = Board.rng.choice([(x, y) for x in range(self.rows)
                                for y in range(self.cols)
                                if self.board[x, y] == '0'])
        if color == 'green':
            self.board[pos] = 'G'
        elif color == 'red':
            self.board[pos] = 'R'
        else:
            raise ValueError("Apple color must be 'green' or 'red'")

    def move_snake(self, direction):
        head_x, head_y = self.snake[0]

        if direction == 'up':
            new_head = (head_x - 1, head_y)
        elif direction == 'down':
            new_head = (head_x + 1, head_y)
        elif direction == 'left':
            new_head = (head_x, head_y - 1)
        elif direction == 'right':
            new_head = (head_x, head_y + 1)
        else:
            raise ValueError(
                "Direction must be 'up', 'down', 'left', or 'right'")

        if self.is_oob(new_head) or self.board[new_head] == 'S':
            return 'dead'

        tile = self.board[new_head]
        self.snake.appendleft(new_head)
        self.board[new_head] = 'H'
        self.board[head_x, head_y] = 'S'

        if tile == 'G':
            self.place_apple('green')
            return 'green'
        if tile == 'R':
            if len(self.snake) == 1:
                return 'dead'
            self.board[self.snake.pop()] = '0'
            self.board[self.snake.pop()] = '0'
            self.place_apple('red')
            return 'red'

        self.board[self.snake.pop()] = '0'
        return 'clear'
