import pygame

import swordsman
import castle
import cavalry
import landscapes


class Screen:
    def __init__(self, size):
        self.sc = pygame.display.set_mode(size)
        self.choose_unit = None
        self.icon_swordsman = swordsman.Swordsman(125, 25, 80,
                                                  swordsman.swordsmans)
        self.icon_cavalry = cavalry.Cavalry(125, 125, 80, cavalry.cavalrys)

    def choose_unit(self, mouse_pos):
        if (self.icon_swordsman.rect.left <= mouse_pos[0] <= self.icon_swordsman.rect.right and
                self.icon_swordsman.rect.top <= mouse_pos[1] <= self.icon_swordsman.rect.bottom):
            self.choose_unit = 'swordsman'
        if (self.icon_cavalry.rect.left <= mouse_pos[0] <= self.icon_cavalry.rect.right and
                self.icon_cavalry.rect.top <= mouse_pos[1] <= self.icon_cavalry.rect.bottom):
            self.choose_unit = 'cavalry'
        return self.choose_unit

    def render(self, board):
        landscapes.grasses.draw(self.sc)
        board.render(self.sc)
        castle.castles.draw(self.sc)
        swordsman.swordsmans.draw(self.sc)
        swordsman.set_view_stock(self.sc, (50, 50))
        cavalry.cavalrys.draw(self.sc)
        cavalry.set_view_stock(self.sc, (50, 150))


class Board:
    def __init__(self, width, height, size):
        self.sc = Screen(size)
        self.width = width
        self.height = height
        self.set_view()

        self.board = [[0] * width for _ in range(height)]

        self.choosen_unit = None

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == (0, 4):
                    castle.add_start_castle(i * self.cell_size + self.left, j * self.cell_size + self.top,
                                            self.cell_size)
                    self.board[j][i], self.board[j][i + 1], self.board[j + 1][i], self.board[j + 1][i + 1] = 1, 1, 1, 1

    def set_view(self):
        self.cell_size = 60
        self.left = 250
        self.top = 50

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top

                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), 1)

                landscapes.Grass(x, y, self.cell_size, landscapes.grasses)

    def get_cell(self, mouse_pos):
        xmax = self.left + self.width * self.cell_size
        ymax = self.top + self.height * self.cell_size
        if not (self.left < mouse_pos[0] < xmax and self.top < mouse_pos[1] < ymax):
            return -1, -1
        n_x = (mouse_pos[0] - self.left) // self.cell_size
        n_y = (mouse_pos[1] - self.top) // self.cell_size

        return n_x, n_y

    def on_click(self, cell_coords, mouse_button):
        x, y = cell_coords
        if mouse_button == 1:
            if self.choosen_unit == 'swordsman' and self.board[y][x] == 0 and swordsman.stock > 0:
                swordsman.Swordsman(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                    swordsman.swordsmans)
                swordsman.stock -= 1
                self.board[y][x] = 1

            if self.choosen_unit == 'cavalry' and self.board[y][x] == 0 and cavalry.stock > 0:
                cavalry.Cavalry(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                cavalry.cavalrys)
                cavalry.stock -= 1
                self.board[y][x] = 1
        elif mouse_button == 3:
            pass  # правой кнопкой мыши - удалить и вернуть единицу в инвентарь

    def get_click(self, mouse_pos, mouse_button):
        cell = self.get_cell(mouse_pos)
        if cell[0] >= 0 and cell[1] >= 0:
            self.on_click(cell, mouse_button)
        self.choosen_unit = Screen.choose_unit(self.sc, mouse_pos)