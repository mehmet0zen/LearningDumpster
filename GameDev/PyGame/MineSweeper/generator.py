import random

class Generate:
    def __init__(self, size: int = 16, difficulty: int = 15):
        self.size = size
        self.difficulty = difficulty
    
    def start_generating(self):
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        self.mines = []
        self.generate_mines()
        self.generate_numbers()

    def generate_mines(self):
        for i in range(self.difficulty):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if [x, y] not in self.mines:
                self.mines.append([x, y])
    
    def generate_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if [i, j] in self.mines:
                    self.board[i][j] = -1
                else:
                    self.board[i][j] = self.count_mines(i, j)
                    
    def count_mines(self, x: int, y: int):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.check_bounds(x + i, y + j):
                    if [x + i, y + j] in self.mines:
                        count += 1
        return count
    
    def check_bounds(self, x: int, y: int):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        return True
    
    def print_board(self):
        output = ''
        for i in range(self.size):
            for j in range(self.size):
                output += str(self.board[i][j]) + ' '
            output += '\n'
        print(output)
