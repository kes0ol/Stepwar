import pygame

import swordsman
import castle


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.set_view()
        self.board = [[0] * width for _ in range(height)]

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == (0, 5):
                    castle.add_start_castle(i * self.cell_size + self.left, j * self.cell_size + self.top,
                                            self.cell_size)

    def set_view(self):
        self.cell_size = 60
        self.left = 200
        self.top = 50

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top

                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        xmax = self.left + self.width * self.cell_size
        ymax = self.top + self.height * self.cell_size
        if not (self.left < mouse_pos[0] < xmax and self.top < mouse_pos[1] < ymax):
            return -1, -1
        n_x = (mouse_pos[0] - self.left) // self.cell_size
        n_y = (mouse_pos[1] - self.top) // self.cell_size

        return n_x, n_y

    def on_click(self, cell_coords):
        x, y = cell_coords
        if self.board[y][x] == 0:
            swordsman.Swordsman(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                swordsman.swordsmans)
            self.board[y][x] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell[0] >= 0 and cell[1] >= 0:
            self.on_click(cell)
