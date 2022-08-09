import pygame
import os
import sys
import generate
from collections import deque

class drawNumPuzz(generate.NumPuzz):
    def __init__(self, size, screen, bg1, bg2, font: pygame.font.SysFont):
        super().__init__(size)
        self.screen = screen
        self.bg1 = bg1
        self.bg2 = bg2
        self.generate()
        self.block_size = screen.get_width() / size
        self.font = font
    
    def draw(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.puzzle[row][column] != 0:
                    self.draw_block(self.bg1, row, column)
                else:
                    self.draw_block(self.bg2, row, column)
        pygame.display.update() 
    
    def draw_block(self, color, row, column, outline_color = (235, 91, 77)):
        pygame.draw.rect(self.screen, color, (row * self.block_size, column * self.block_size, self.block_size, self.block_size))
        pygame.draw.rect(self.screen, outline_color, (row * self.block_size, column * self.block_size, self.block_size, self.block_size), 1)
        text = self.font.render(str(self.puzzle[row][column]), True, (0, 0, 0))
        if self.puzzle[row][column] != 0:
            self.screen.blit(text, (row * self.block_size + self.block_size // 2 - text.get_width()//2, column*self.block_size+self.block_size//2-text.get_height()//2))

    def __move_block(self, row, column):
        temp = [row, column]
        if row == self.zero_pos[0]:
            if column <= self.zero_pos[1]:
                temp[1] = self.zero_pos[1] - 1
            else:
                temp[1] = self.zero_pos[1] + 1
        elif column == self.zero_pos[1]:
            if row < self.zero_pos[0]:
                temp[0] = self.zero_pos[0] - 1
            else:
                temp[0] = self.zero_pos[0] + 1
        if self.area_has_zero(row, column):
            self.puzzle[self.zero_pos[0]][self.zero_pos[1]] = self.puzzle[temp[0]][temp[1]]
            self.puzzle[temp[0]][temp[1]] = 0
            self.zero_pos = (temp[0], temp[1])
        return

    def move_blocks(self, pos: (int, int)):
        row, column = list(pos)
        row //= (self.screen.get_width() // self.size)
        column //= (self.screen.get_width() // self.size)
        if not self.area_has_zero(row, column):
            return
        if self.check_win():
            print("You win!")
            return
        while (row, column) != self.zero_pos:
            self.__move_block(row, column)
        self.draw()

    def area_has_zero(self, row, column) -> bool:
        return row == self.zero_pos[0] or column == self.zero_pos[1]
    
    def check_win(self) -> bool:
        puzzle = ''
        final = ''.join(str(i) for i in range(1, self.size**2))
        for j in range(self.size):
            for i in range(self.size):
                puzzle += str(self.puzzle[i][j])
        return puzzle.replace('0', '') == final