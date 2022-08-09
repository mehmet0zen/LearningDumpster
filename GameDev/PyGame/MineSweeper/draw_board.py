import generator
import random
import pygame
import math
import colorsys

class Draw(generator.Generate):
    def __init__(self, *, screen: pygame.surface, size: int = 16, difficulty: int = 15, mine_image: pygame.image = None, flag_image: pygame.image = None, padding_left: int = 0, padding_right: int = 0, color_block_1_hsv: tuple = (108, 13, 92), color_block_2_hsv: tuple = (132, 28, 93)):
        super().__init__(size, difficulty)
        self.screen = screen
        self.start_generating()
        self.padding_left = padding_left
        self.padding_right = padding_right
        self.block_size = (self.screen.get_width() - self.padding_left - self.padding_right) / self.size
        if mine_image:
            self.mine_img = pygame.transform.scale(mine_image, (self.block_size / 1.5, self.block_size / 1.5))
        if flag_image:
            self.flag_img = pygame.transform.scale(flag_image, (self.block_size, self.block_size))
        self.font = pygame.font.SysFont('comicsans', int(self.block_size // 2))
        self.revealed_blocks = []
        self.flaged_blocks = []
        self.zeros = []
        self.chained_zeros = []
        self.zero_areas = self.area_zeros()
        self.color_hue = random.randint(10, 50)
        self.color_block_1 = color_block_1_hsv
        self.color_block_2 = color_block_2_hsv
        self.mistake = None
        self.game_state = 'playing'
    
    def draw_board(self, with_numbers = True):
        self.screen.fill((255, 255, 255))
        if not with_numbers:
            for row in range(self.size):
                for column in range(self.size):
                    if (column + row) % 2 == 0:
                        pygame.draw.rect(self.screen, self.hsv_to_rgb(self.color_block_1), (row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size))
                    else:
                        pygame.draw.rect(self.screen, self.hsv_to_rgb(self.color_block_2), (self.padding_left + row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size))
            return
        for row in range(self.size):
            for column in range(self.size):
                if (row, column) in self.zeros:
                    if  (column + row) % 2 == 0:
                        pygame.draw.rect(self.screen, self.get_num_color(1, self.color_block_1[0], self.color_block_1[1] - 2, self.color_block_1[2] - 18), (row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size))
                    else:
                        pygame.draw.rect(self.screen, self.get_num_color(1, self.color_block_2[0] - 1, self.color_block_2[1], self.color_block_2[2] - 18), (row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size))
                else:
                    if (column + row) % 2 == 0:
                        pygame.draw.rect(self.screen, self.hsv_to_rgb(self.color_block_1), (row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size))
                    else:
                        pygame.draw.rect(self.screen, self.hsv_to_rgb(self.color_block_2), (self.padding_left + row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size))
                if (row, column) == self.mistake:
                    pygame.draw.rect(self.screen, (235, 87, 104), (row * self.block_size, (self.padding_left + column - self.padding_right) * self.block_size, self.block_size, self.block_size), 6, 15)
                if ((row, column) not in self.revealed_blocks or self.board[row][column] == 0) and (row, column) not in self.flaged_blocks:
                    continue
                self.draw_num(row, column)
        pygame.display.update()
    
    def draw_num(self, row, column):
        num = self.board[row][column]
        if (row, column) in self.flaged_blocks and (row, column) not in self.zeros:
            if self.flag_img:
                return self.screen.blit(self.flag_img, (row * self.block_size + self.block_size / 2 - self.flag_img.get_width() / 2, (self.padding_left + column - self.padding_right) * self.block_size + self.block_size / 2 - self.flag_img.get_height() / 2))
            else:
                text = self.font.render('#', True, (102, 209, 96))
        elif num == 0: text = self.font.render('', True, (59, 59, 59))
        elif num == -1: 
            if self.mine_img:
                return self.screen.blit(self.mine_img, (row * self.block_size + self.block_size / 2 - self.mine_img.get_width() / 2, (self.padding_left + column - self.padding_right) * self.block_size + self.block_size / 2 - self.mine_img.get_height() / 2))
            else: 
                text = self.font.render('*', True, (255, 0, 0))
        else: text = self.font.render(str(num), True, self.get_num_color(num, self.color_hue))
        self.screen.blit(text, (row * self.block_size + self.block_size / 2 - text.get_width() / 2, (self.padding_left + column - self.padding_right) * self.block_size + self.block_size / 2 - text.get_height() / 2))
     
    def set_block_hsv(self, color_block_1_hsv, color_block_2_hsv):
        self.color_block_1 = color_block_1_hsv
        self.color_block_2 = color_block_2_hsv
     
    def get_num_color(self, num: int, h = 20, s = 50, v = 70) -> tuple:
        h = num * h
        if h > 360:
            h -= 360
        return self.hsv_to_rgb((h, s, v))
    
    def hsv_to_rgb(self, color_hsv):
        h, s, v = color_hsv
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100))
    
    def select_block(self, x: int, y: int):
        if not self.check_bounds(x, y):
            return
        if (x, y) in self.flaged_blocks:
            self.flag_block(x, y)
            return self.draw_board()
        if self.board[x][y] == -1:
            self.game_state = 'lost'
            self.mistake = (x, y)
            self.revealed_blocks += [(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == -1]
            return self.draw_board()
        if self.board[x][y] == 0:
            self.chained_zeros = [(x, y)]
            area_zero = []
            for areas in self.zero_areas:
                if any(chain in areas for chain in self.chained_zeros):
                    area_zero += areas
            self.add_to_zeros(area_zero)
            self.zeros += area_zero
            if self.game_won():
                self.game_state = 'won'
                self.flaged_blocks = [(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == -1]
            self.draw_board()
        else:
            self.revealed_blocks.append((x, y))
            if self.game_won():
                self.game_state = 'won'
                self.flaged_blocks = [(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == -1]
            self.draw_board()
    
    def game_won(self):
        return len(list(set(self.revealed_blocks))) == self.size ** 2 - sum([x.count(-1) for x in self.board]) or sorted(self.flaged_blocks) == sorted([(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == -1])
    
    def flag_block(self, x: int, y: int):
        if (x, y) in self.flaged_blocks:
            self.flaged_blocks.remove((x, y))
        else:
            self.flaged_blocks.append((x, y))
        self.draw_board()
            
    def area_zeros(self):
        zeros = []
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] != 0:
                    continue
                count = 0
                for x in range(len(zeros)):
                    if self.board[row][column] != 0:
                        continue
                    if self.check_bounds(row - 1, column) and (row - 1, column) in zeros[x]:
                        zeros[x].append((row, column))
                        if any(pz in zeros[x] for pz in self.chained_zeros):
                            self.chained_zeros.append((row, column))
                    if self.check_bounds(row, column - 1) and (row, column - 1) in zeros[x]:
                        zeros[x].append((row, column))
                        if any(pz in zeros[x] for pz in self.chained_zeros):
                            self.chained_zeros.append((row, column))
                    if self.check_bounds(row + 1, column) and (row + 1, column) in zeros[x]:
                        zeros[x].append((row, column))
                        if any(pz in zeros[x] for pz in self.chained_zeros):
                            self.chained_zeros.append((row, column))
                    if self.check_bounds(row, column + 1) and (row, column + 1) in zeros[x]:
                        zeros[x].append((row, column))
                        if any(pz in zeros[x] for pz in self.chained_zeros):
                            self.chained_zeros.append((row, column))
                    count += 1
                if count >= len(zeros):
                    zeros.append([(row,column)])
        return zeros
    
    def add_to_zeros(self, area_zero):
        for x, y in area_zero:
            if self.check_bounds(x - 1, y):
                self.revealed_blocks.append((x - 1, y))
                if self.board[x - 1][y] == 0 and (x - 1, y) not in area_zero:
                    area_zero.append((x - 1, y))
            if self.check_bounds(x + 1, y):
                self.revealed_blocks.append((x + 1, y))
                if self.board[x + 1][y] == 0 and (x + 1, y) not in area_zero:
                    area_zero.append((x + 1, y))
            if self.check_bounds(x, y - 1):
                self.revealed_blocks.append((x, y - 1))
                if self.board[x][y - 1] == 0 and (x, y - 1) not in area_zero:
                    area_zero.append((x, y - 1))
            if self.check_bounds(x, y + 1):
                self.revealed_blocks.append((x, y + 1))
                if self.board[x][y + 1] == 0 and (x, y + 1) not in area_zero:
                    area_zero.append((x, y + 1))
            #corners
            if self.check_bounds(x + 1, y + 1):
                self.revealed_blocks.append((x + 1, y + 1))    
                if self.board[x + 1][y + 1] == 0 and (x + 1, y + 1) not in area_zero:
                    area_zero.append((x + 1, y + 1))
            if self.check_bounds(x - 1, y + 1):
                self.revealed_blocks.append((x - 1, y + 1))    
                if self.board[x - 1][y + 1] == 0 and (x - 1, y + 1) not in area_zero:
                    area_zero.append((x - 1, y + 1))
            if self.check_bounds(x - 1, y - 1):
                self.revealed_blocks.append((x - 1, y - 1))    
                if self.board[x - 1][y - 1] == 0 and (x - 1, y - 1) not in area_zero:
                    area_zero.append((x - 1, y - 1))
            if self.check_bounds(x + 1, y - 1):
                self.revealed_blocks.append((x + 1, y - 1))    
                if self.board[x + 1][y - 1] == 0 and (x + 1, y - 1) not in area_zero:
                    area_zero.append((x + 1, y - 1))
                
    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = int((event.pos[0] + self.padding_left - self.padding_right) / self.block_size)
            y = int((event.pos[1]) / self.block_size)
            if event.button == 1 and self.game_state == 'playing':
                self.select_block(x, y)
            if event.button == 3 and self.game_state == 'playing':
                self.flag_block(x, y)
                