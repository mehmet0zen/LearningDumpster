import random
import sys

class NumPuzz:
    def __init__(self, size):
        self.size = size
        self.puzzle = []
        self.zero_pos = (0, 0)
    
    def generate(self):
        self.all_nums = [i for i in range(1, self.size**2)]
        self.all_nums.append(0)
        self.puzzle = [[0 for x in range(self.size)] for y in range(self.size)]
        self.fill_puzzle()
        return self.puzzle
    
    def fill_puzzle(self):
        for i in range(self.size):
            for j in range(self.size):
                temp = random.choice(self.all_nums)
                self.puzzle[i][j] = temp
                self.all_nums.remove(temp)
                if temp == 0:
                    self.zero_pos = (i, j)
        return self.puzzle

    def __str__(self):
        return str(self.puzzle)
    
    def __repr__(self):
        return str(self.puzzle)
    
    def is_solvable(self):
        # TODO: Check if puzzle is solvable!
        pass