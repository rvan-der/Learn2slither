import numpy as np
from collections import deque


class Board:

    rng = np.random.default_rng()

    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.board = np.full((rows, cols), '0', dtype=str)
        self.snake = deque()
        self.initialize_board()

    def is_oob(self, position):  # oob = out of bounds
        row, col = position
        return row < 0 or row >= self.rows or col < 0 or col >= self.cols

    def move_coords(self, position, direction):
        row, col = position
        if direction == 'up':
            return (row - 1, col)
        if direction == 'down':
            return (row + 1, col)
        if direction == 'left':
            return (row, col - 1)
        if direction == 'right':
            return (row, col + 1)
        raise ValueError("Direction must be 'up', 'down', 'left', or 'right'")

    def initialize_board(self):
        pos = tuple(self.rng.choice([(y, x) for y in range(self.rows)
                                    for x in range(self.cols)]))
        self.snake.append(pos)
        self.board[pos] = 'H'
        for _ in range(2):
            moved = ()
            directions = ['up', 'down', 'left', 'right']
            while True:
                dir = self.rng.choice(directions)
                moved = self.move_coords(pos, dir)
                if self.is_oob(moved) or self.board[moved] != '0':
                    directions.remove(dir)
                else:
                    pos = moved
                    break
            self.snake.append(pos)
            self.board[pos] = 'S'

        self.place_apple('G')
        self.place_apple('G')
        self.place_apple('R')

    def place_apple(self, character):
        pos = tuple(self.rng.choice([(y, x) for y in range(self.rows)
                                    for x in range(self.cols)
                                    if self.board[y, x] == '0']))
        self.board[pos] = character

    def move_snake(self, direction):
        old_head = self.snake[0]
        new_head = self.move_coords(old_head, direction)

        if self.is_oob(new_head) or self.board[new_head] == 'S':
            return 'dead'

        tile = self.board[new_head]
        self.snake.appendleft(new_head)
        self.board[new_head] = 'H'
        self.board[old_head] = 'S'

        if tile == 'G':
            self.place_apple('G')
            return 'green'

        self.board[self.snake.pop()] = '0'
        if tile == 'R':
            if len(self.snake) == 1:
                return 'dead'
            self.board[self.snake.pop()] = '0'
            self.place_apple('R')
            return 'red'

        return 'clear'

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.board)


if __name__ == "__main__":
    board = Board(10, 10)
    print(board, end='\n\n')
    while True:
        direction = ''
        d = input("direction: ")
        if d == 'z':
            direction = 'up'
        elif d == 's':
            direction = 'down'
        elif d == 'q':
            direction = 'left'
        elif d == 'd':
            direction = 'right'
        else:
            print("invalid direction")
            continue
        status = board.move_snake(direction)
        print(board)
        if status == 'dead':
            print(status)
            break
        else:
            print(status, end='\n\n')
