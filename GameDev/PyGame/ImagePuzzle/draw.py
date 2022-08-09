import pygame
import os
import sys
import generate
from collections import deque

class drawNumPuzz(generate.NumPuzz):
    def __init__(self, size, screen, font: pygame.font.SysFont, image_path: str):
        super().__init__(size)
        self.screen = screen
        self.generate()
        self.block_size = screen.get_width() / size
        self.font = font
        self.image_path = image_path
        self.__slice_image(image_path)
    
    def draw(self):
        for row in range(self.size):
            for column in range(self.size):
                self.draw_block(row, column)
        pygame.display.update() 
    
    def draw_block(self, row, column):
        if self.puzzle[row][column] != 0:
            self.screen.blit(self.images[self.puzzle[row][column]], (row * self.block_size, column * self.block_size))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (row * self.block_size, column * self.block_size, self.block_size, self.block_size))
    
    def __slice_image(self, image_path):
        self.images = {}
        sheet = pygame.image.load(image_path)
        image = pygame.Surface((self.screen.get_width(), self.screen.get_width())).convert_alpha()
        image = pygame.transform.scale(sheet, (self.screen.get_width(), self.screen.get_width()))
        for i in range(self.size):
            for j in range(self.size):
                self.images[i*self.size + j + 1] = image.subsurface((j * self.block_size, i * self.block_size, self.block_size, self.block_size))
     
    def draw_preview(self):
        image = pygame.image.load(self.image_path)
        image = pygame.transform.scale(image, (self.screen.get_width(), self.screen.get_width()))
        self.screen.blit(image, (0, 0))
        prev_text = pygame.font.SysFont("comicsansms", 15).render("preview on", True, (255, 0, 0))
        self.screen.blit(prev_text, (self.screen.get_width() - prev_text.get_width() - 10, 10))
        pygame.display.update()
                 
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
        if not self.area_has_zero(row, column) or row >= self.size or column >= self.size:
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