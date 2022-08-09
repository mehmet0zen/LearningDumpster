import random
import math
import sys
import collections
import json
import os
import copy

class Generate:
    def __init__(self, size: int = 9, difficulty = 12):
        self.size = 9 if size <= 3 else int(math.sqrt(size)) ** 2
        self.difficulty = difficulty
        file_path = os.path.dirname(os.path.realpath(__file__))
        self.templates_path = file_path + '/.templates.txt'
        self.vertical_lines = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(self.size)]
        self.horizontal_lines = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(self.size)]
        self.empty_cell_pos = []
    
    def generate_numbers(self):
        templates = {}
        if os.path.exists(self.templates_path) and os.path.getsize(self.templates_path) > 0:
            with open(self.templates_path, 'r') as f:
                templates = json.load(f)
        if templates.get(str(self.size)) == None:
            templates[str(self.size)] = self.create_template()
        
        self.generated_numbers = self.shuffle_template(templates[str(self.size)])
        with open(self.templates_path, 'w') as f:
            templates[str(self.size)] = self.generated_numbers
            data = json.dumps(templates)
            f.write(data)
    
    def shuffle_template(self, template) -> [int]:
        self.vertical_lines = self.shuffle_lines(template)
        self.horizontal_lines = self.shuffle_lines(self.rotate(self.vertical_lines))
        self.vertical_lines = self.rotate(self.horizontal_lines)
        return self.vertical_lines

    def shuffle_lines(self, lines):
        blocks = []
        for i, l in enumerate(lines):
            if i % int(math.sqrt(self.size)) == 0:
                blocks += [[l]]
            else:
                blocks[-1] += [l]
        random.shuffle(blocks)
        
        lines = []
        for i, b in enumerate(blocks):
            random.shuffle(blocks[i])
            for j in b:
                lines += [j]
        return lines
      
    def create_template(self) -> [int]:
        nums = [i for i in range(1, self.size + 1)]
        random.shuffle(nums)
        numbers = collections.deque(nums)
        template = []
        for i in range(self.size):
            number = 0
            if i % int(math.sqrt(self.size)) == 0 and i != 0:
                numbers.rotate(1)
            while number < self.size:
                if len(template) > i:
                    template[i].append(list(numbers)[number])
                else:
                    template.append([list(numbers)[number]])
                number += 1
            numbers.rotate(int(math.sqrt(self.size)))
        return template
        
    def rotate(self, lines: [[int]]) -> [[int]]:
        rotated_lines = []
        for i in range(len(lines[0])):
            rotated_lines.append([])
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                rotated_lines[j].append(lines[i][j])
        return rotated_lines
    
    def remove_nums(self):
        final_numbers = copy.deepcopy(self.vertical_lines)
        self.empty_cell_pos = []
        for i in range(self.difficulty): 
            rand_row = random.randint(0, self.size - 1)
            rand_column = random.randint(0, self.size - 1)
            while final_numbers[rand_row][rand_column] == 0:
                rand_row = random.randint(0, self.size - 1)
                rand_column = random.randint(0, self.size - 1)
            final_numbers[rand_row][rand_column] = 0
            self.empty_cell_pos.append((rand_row, rand_column))
        self.empty_cells = len(self.empty_cell_pos)
        return final_numbers
    
    def placable_nums(self, horizontal_line: [int], vertical_line: [int], block_nums: [int], size = 9) -> [int]:
        remove_nums = horizontal_line + vertical_line + block_nums
        return [i for i in range(1, size + 1) if i not in remove_nums and i != 0]
    
    def solve_sudoku(self, sudoku, size = 9):
        for i in range(len(sudoku)):
            while len(sudoku[i]) < size:
                sudoku.append(0)
        row_count = 0
        for row in range(len(sudoku)):
            column_count = 0
            if row % int(math.sqrt(size)) == 0 and row != 0: 
                row_count += int(math.sqrt(size))
            for column in range(len(sudoku)):
                if column % int(math.sqrt(size)) == 0 and column != 0:
                    column_count += int(math.sqrt(size))
                vertical_line = [sudoku[i][column] for i in range(len(sudoku))]
                horizontal_line = [sudoku[row][i] for i in range(len(sudoku))]
                block_nums = [sudoku[i][j] for i in range(row_count, row_count + int(math.sqrt(size))) for j in range(column_count, column_count + int(math.sqrt(size)))]
                if (horizontal_line.count(sudoku[row][column]) > 1 or vertical_line.count(sudoku[row][column]) > 1 or block_nums.count(sudoku[row][column]) > 1) and sudoku[row][column] != 0:
                    return 'Invalid sudoku'
                if sudoku[row][column] == 0:
                    if self.placable_nums(horizontal_line, vertical_line, block_nums, size) == []:
                        print(row, column, '\n', horizontal_line, vertical_line, block_nums)
                        return 'No solution'
        sudoku = self.__place_numbers(sudoku, size)
        self.vertical_lines = sudoku
        return 'Solved!'
        
    
    def __place_numbers(self, sudoku, size):
        solved = copy.deepcopy(sudoku)
        row_count = 0
        for row in range(len(solved)):
            column_count = 0
            if row % int(math.sqrt(size)) == 0 and row != 0: 
                row_count += int(math.sqrt(size))
            for column in range(len(solved)):
                if column % int(math.sqrt(size)) == 0 and column != 0:
                    column_count += int(math.sqrt(size))
                vertical_line = [solved[i][column] for i in range(len(solved))]
                horizontal_line = [solved[row][i] for i in range(len(solved))]
                block_nums = [solved[i][j] for i in range(row_count, row_count + int(math.sqrt(size))) for j in range(column_count, column_count + int(math.sqrt(size)))]
                if solved[row][column] == 0:
                    if self.placable_nums(horizontal_line, vertical_line, block_nums, size) == []:
                        print(sudoku)
                        return self.__place_numbers(sudoku, size)
                    solved[row][column] = random.choice(self.placable_nums(horizontal_line, vertical_line, block_nums, size))
        return solved
    def __print_sudoku(self, sudoku):
        for row in sudoku:
            for column in row:
                print(column, end=' ')
            print()
    def output(self, sudoku):
      return [str(column) for column in row for row in sudoku]
  
if __name__ == '__main__':
    g = Generate(9, 1)
    g.generate_numbers()