# import sudoku
import generator
import pygame
import sys
import math
import os

class Draw_board(generator.Generate):
    def __init__(self, screen, board_color: (int), num_color: (int), num_font: str, pygame_screen: pygame.Surface, saved_file: str, selected_color = (225, 255, 156), sudoku_size: int = 9, sudoku_difficulty = 20):
        super().__init__(sudoku_size, sudoku_difficulty)
        self.difficulty = sudoku_difficulty
        self.board_color = board_color
        self.num_color = num_color
        self.selected_color = selected_color
        self.placed_num_pos = []
        self.size = sudoku_size
        self.num_font = num_font
        self.board_size = screen.get_width()
        self.screen = pygame_screen
        self.offset = self.board_size // self.size
        self.empty_block_count = 0
        self.no_empty_blocks = False
        self.checked = False
        self.selected = True
        self.selected_row, self.selected_column = 0, 0
        self.inputted_nums = [0 for i in range(self.size * self.size)]
        self.saved = True

    def __str__(self):
        return self.output(self.generated_numbers)
    def __repr__(self):
        return f'sudoku: {self.output(self.generated_numbers)}'
    
    
    def generate(self, animate = False):
        sys.setrecursionlimit(10000)
        self.generate_numbers()
        self.answer_sheet = self.generated_numbers
        self.vertical_lines = self.remove_nums()
        self.placed_num_pos = []
        self.selected = True
        self.saved = False
        self.selected_column, self.selected_row = 0, 0
        self.draw_sudoku(animate)
        self.empty_block_count = abs(len(self.placed_num_pos) - len(self.empty_cell_pos))
        
    def clear_board(self):
        self.placed_num_pos = []
        self.inputted_nums = [0 for i in range(self.size * self.size)]
        self.vertical_lines = [[0 for i in range(self.size)] for j in range(self.size)]
        self.checked = False
        self.selected_row, self.selected_column = 0, 0
        self.__fill_bg()
    
    def draw_sudoku(self, animate = False):
        for row in range(self.size):
            for column in range(self.size):
                column_point = column * self.offset
                row_point = row * self.offset
                # Draws bold line for every 3 by 3 block
                if (column % int(math.sqrt(self.size)) == 0 and column != 0):
                    pygame.draw.line(self.screen, self.board_color, (column_point, row_point), (column_point, row_point + self.offset), 5)
                if (row % int(math.sqrt(self.size)) == 0 and row != 0): 
                    pygame.draw.line(self.screen, self.board_color, (column_point, row_point), (column_point + self.offset, row_point), 5)
                # Draws every blocks
                pygame.draw.rect(self.screen, self.board_color, (row_point, column_point, self.offset, self.offset), 1)
        self.__draw_nums(animate)
    
    def __draw_nums(self, animate = False):
        for row in range(self.size):
            for column in range(self.size):
                column_point = column * self.offset
                row_point = row * self.offset
                text_padding = self.offset // math.sqrt(self.size)
                # Draws numbers, if 0 then it is empty
                if self.vertical_lines[row][column] != 0:
                    font = pygame.font.Font(self.num_font, 25)
                    # If number has been placed by player, color it selected_color
                    if (row, column) in self.placed_num_pos and not self.checked: 
                        text = font.render(str(self.vertical_lines[row][column]), True, self.num_color, self.selected_color)
                    else: # Else, no background color
                        text = font.render(str(self.vertical_lines[row][column]), True, self.num_color)
                    self.screen.blit(text, (row_point + text_padding, column_point + text_padding))
                if animate:
                    pygame.display.update()
                    pygame.time.delay(10)

    def select_block(self, pos):
        x, y = pos
        if y < self.board_size:
            self.selected_row = int(y / self.offset)
            self.selected_column = int(x / self.offset)
            self.__draw_selected_block(self.selected_row, self.selected_column, self.selected_color)
            self.selected = True
        else:
            self.selected = False
        return self.selected_row, self.selected_column
  
    def input_num(self, num):
        if not self.selected:
            return
        elif self.vertical_lines[self.selected_column][self.selected_row] == 0 or (self.selected_column, self.selected_row) in self.placed_num_pos:
            self.__fill_grid_bg()
            if num in range(1, 10) and (self.selected_column, self.selected_row) not in self.placed_num_pos:
                self.placed_num_pos.append((self.selected_column, self.selected_row))
            self.vertical_lines[self.selected_column][self.selected_row] = num
            self.inputted_nums[self.selected_row * self.size + self.selected_column] = num
            self.draw_sudoku()
            self.__draw_selected_block(self.selected_row, self.selected_column, self.selected_color)
        # check if empty blocks are left
        self.no_empty_blocks = len(self.placed_num_pos) == len(list(set(self.empty_cell_pos)))
        self.saved = False

    def remove_num(self):
        if (self.selected_column, self.selected_row) in self.placed_num_pos and self.selected and self.vertical_lines[self.selected_column][self.selected_row] != 0:
            self.input_num(0)
            self.placed_num_pos.remove((self.selected_column, self.selected_row))

    def my_score(self, color_lost: (int), color_won: (int), animate=True):
        self.color_lost = color_lost
        self.color_won = color_won
        score = 0
        if not self.no_empty_blocks and not self.checked:
            return
        self.__fill_bg(animate=False)
        for i in self.placed_num_pos:
            column, row = i
            font = pygame.font.Font(self.num_font, 25)
            text_padding = self.offset // math.sqrt(self.size)
            num = self.vertical_lines[column][row]
            if num != 0:
                if self.answer_sheet[column][row] == num:
                    self.__draw_selected_block(row, column, color_won, 0, True)
                    text = font.render(str(num), True, self.num_color)
                    score += 1
                else:
                    self.__draw_selected_block(row, column, color_lost, 0, True)
                    text = font.render(str(num), True, self.num_color)
                self.screen.blit(text, (column * self.offset + text_padding, row * self.offset + text_padding))
                if animate:
                    pygame.display.update()
                    pygame.time.delay(10)
        self.checked = True
        self.selected = False
        return score

    def jump_to_next_empty_block(self):
        if self.checked:
            return
        self.__next_block_pos()
        while (self.selected_column, self.selected_row) not in self.empty_cell_pos:
            self.__next_block_pos()
        self.__draw_selected_block(self.selected_row, self.selected_column, self.selected_color)
        pygame.display.update()

    def __next_block_pos(self):
        if self.selected_column < self.size - 1:
            self.selected_column += 1
        else:
            self.selected_column = 0
            if self.selected_row < self.size - 1:
                self.selected_row += 1
            else:
                self.selected_row = 0

    def __prev_block_pos(self):
        if self.selected_column > 0:
            self.selected_column -= 1
        else:
            self.selected_column = self.size - 1
            if self.selected_row > 0:
                self.selected_row -= 1
            else:
                self.selected_row = self.size - 1
    
    def move_with_arrows(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.selected:
                return
            if event.key == pygame.K_RIGHT:
                if self.selected_column == self.size - 1:
                    self.selected_column = 0
                else:
                    self.selected_column += 1
            if event.key == pygame.K_UP:
                if self.selected_row == 0:
                    self.selected_row = self.size - 1
                else:
                    self.selected_row -= 1
            if event.key == pygame.K_DOWN:
                if self.selected_row == self.size - 1:
                    self.selected_row = 0
                else:
                    self.selected_row += 1
            if event.key == pygame.K_LEFT:
                if self.selected_column == 0:
                    self.selected_column = self.size - 1
                else:
                    self.selected_column -= 1
            if event.key in [pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT]:
                self.checked = False
                self.__draw_selected_block(self.selected_row, self.selected_column, self.selected_color)
                self.selected = True
    
    def new_game(self, saved_file: str, remove_saved = False, animate = True):
        self.placed_num_pos = []
        self.generate_numbers()
        self.vertical_lines = self.remove_nums()
        self.answer_sheet = self.generated_numbers
        self.selected = True
        self.saved = False
        self.selected_column, self.selected_row = 0, 0
        self.empty_block_count = len(self.empty_cell_pos)
        self.__fill_grid_bg()
        self.draw_sudoku(animate)
        pygame.display.update()
        if os.path.exists(saved_file) and remove_saved:
            with open(saved_file, "w") as f:
                f.write('')
        
    def solve_my_sudoku(self):
        if self.placed_num_pos == []:
            return 'No numbers placed'
        if self.no_empty_blocks:
            if self.__placed_correctly():
                return 'Correct'
            else:
                return 'Incorrect'
        text = self.solve_sudoku(self.vertical_lines, self.size)
        if text == 'Solved!':
            self.__place_inputted_nums()
            self.__fill_bg()
            self.draw_sudoku()
            self.checked = True
        return text
    
    def block_num(self, row, column) -> int:
        return int(row // math.sqrt(self.size) * (math.sqrt(self.size)) + column // math.sqrt(self.size))

    def save_game(self, file_name: str):
        data = str(self.generated_numbers) + "\n" + str(self.vertical_lines) + '\n' + str(self.inputted_nums) + "\n" + str(self.placed_num_pos) + "\n" + str(self.answer_sheet) + '\n' + str(self.checked) + '\n' + str(self.size) + '\n' + str(self.difficulty) + '\n' + str(self.empty_cell_pos)
        if self.checked:
            data += '\n' + str(self.color_lost) + '\n' + str(self.color_won)
        with open(file_name, "w") as f:
            f.write(data)
        self.saved = True

    def load_game(self, file_name: str):
        with open(file_name, "r") as f:
            self.generated_numbers = eval(f.readline())
            self.vertical_lines = eval(f.readline())
            self.inputted_nums = eval(f.readline())
            self.placed_num_pos = eval(f.readline())
            self.answer_sheet = eval(f.readline())
            self.checked = eval(f.readline())
            self.size = eval(f.readline())
            self.difficulty = eval(f.readline())
            self.empty_cell_pos = eval(f.readline())
            if self.checked:
                self.color_lost = eval(f.readline())
                self.color_won = eval(f.readline())
                self.my_score(self.color_lost, self.color_won, False)
            else:
                self.__fill_grid_bg()
                self.draw_sudoku(True)
            self.empty_block_count = self.vertical_lines.count(0)
        if len(self.empty_cell_pos) == 0:
            for row in range(len(self.vertical_lines)):
                for column in range(len(self.vertical_lines[row])):
                    if self.vertical_lines[row][column] == 0 or (column, row) in self.placed_num_pos:
                        self.empty_cell_pos.append((row, column))
        self.no_empty_blocks = len(self.empty_cell_pos) == len(self.inputted_nums)

    def __fill_grid_bg(self, color: (int) = (255, 255, 255)):
        [pygame.draw.rect(self.screen, color, (row * self.offset, column * self.offset, self.offset, self.offset)) for column in range(self.size) for row in range(self.size)]

    def __fill_bg(self, color: (int) = (255, 255, 255), animate = True):
        pygame.draw.rect(self.screen, color, (0, 0, self.screen.get_width(), self.screen.get_height()))
        self.draw_sudoku(animate = animate)

    def __draw_selected_block(self, row, column, color: (int) = (0, 0, 0), width = 2, draw_multiple = False):
        if not draw_multiple:
            self.__fill_grid_bg()
        self.draw_sudoku()
        pygame.draw.rect(self.screen, color, (column * self.offset, row * self.offset, self.offset, self.offset), width)
        if draw_multiple:
            self.__draw_nums()
        pygame.display.update()
        
    def __place_inputted_nums(self):
        input_nums = [i for i in self.inputted_nums if i != 0]
        for i in range(len(input_nums)):
            column, row = self.placed_num_pos[i]
            self.vertical_lines[column][row] = input_nums[i]
        self.placed_num_pos = []
        return self.vertical_lines
    
    def __placed_correctly(self) -> bool:
        vl, hl, bl = [], [], []
        for i in range(len(self.placed_num_pos)):
            column, row = self.placed_num_pos[i]
            pos_num = (row * self.size) + column
            try:
                vl[column].append(self.inputted_nums[pos_num])
            except:
                while len(vl) < column:
                    vl.append([])
                vl.insert(column, [self.inputted_nums[pos_num]])
            try:
                hl[row].append(self.inputted_nums[pos_num])
            except:
                while len(hl) < row:
                    hl.append([])
                hl.insert(row, [self.inputted_nums[pos_num]])
            try:
                bl[self.block_num(row, column)].append(self.inputted_nums[pos_num])
            except:
                while len(bl) < self.block_num(row, column):
                    bl.append([])
                bl.insert(self.block_num(row, column), [self.inputted_nums[pos_num]])
        vl_check = [len(set(vl[i])) == len(vl[i]) for i in range(len(vl))]
        hl_check = [len(set(hl[i])) == len(hl[i]) for i in range(len(hl))]
        bl_check = [len(set(bl[i])) == len(bl[i]) for i in range(len(bl))]
        return all(vl_check) and all(hl_check) and all(bl_check)