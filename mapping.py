import pygame

import swordsman
import castle
import cavalry
import landscapes


class Screen:
    def __init__(self, size):
        self.sc = pygame.display.set_mode(size)
        self.choose_unit = None
        self.board = Board(18, 10)
        self.button_start_game = Button(38, 200, 26, 1100, 700)
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

    def render(self, board, button_start_game):
        landscapes.grasses.draw(self.sc)
        board.render(self.sc)
        castle.castles.draw(self.sc)
        swordsman.swordsmans.draw(self.sc)
        swordsman.set_view_stock(self.sc, (50, 50))
        cavalry.cavalrys.draw(self.sc)
        cavalry.set_view_stock(self.sc, (50, 150))

        button_start_game.render(self.sc)

    def get_click(self, mouse_pos, mouse_button):
        Board.get_click(self.board, mouse_pos, mouse_button, self)
        if (self.button_start_game.button_rect.left <= mouse_pos[0] <= self.button_start_game.button_rect.right
                and
                self.button_start_game.button_rect.top <= mouse_pos[1] <= self.button_start_game.button_rect.bottom):
            self.button_start_game.gameplay = True


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.cell_size = 60
        self.left = 250
        self.top = 50

        self.board = [[0] * width for _ in range(height)]
        self.landscape = [[0] * width for _ in range(height)]

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == (0, 4):
                    castle.add_start_castle(i * self.cell_size + self.left, j * self.cell_size + self.top,
                                            self.cell_size)
                    self.board[j][i], self.board[j][i + 1], self.board[j + 1][i], self.board[j + 1][i + 1] = 1, 1, 1, 1

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top

                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), 1)
                if self.landscape[i][j] == 0:
                    landscapes.Grass(x, y, self.cell_size, landscapes.grasses)
                    self.landscape[i][j] = 1

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

    def get_click(self, mouse_pos, mouse_button, screen):
        cell = self.get_cell(mouse_pos)
        self.choosen_unit = Screen.choose_unit(screen, mouse_pos)
        if cell[0] >= 0 and cell[1] >= 0:
            self.on_click(cell, mouse_button)


class Button:
    def __init__(self, size_font, surface_x, surface_y, rect_x, rect_y):
        self.gameplay = False
        self.font = pygame.font.Font(None, size_font)
        self.button_surface = pygame.Surface((surface_x, surface_y))
        self.text = self.font.render("Начать игру", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.rect_width = self.text_rect.width
        self.rect_height = self.text_rect.height
        self.button_rect = pygame.Rect(rect_x, rect_y, self.rect_width, self.rect_height)

    def check_collidepoint(self, rect_width, rect_height):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.button_surface, (0, 200, 0), (0, 0, rect_width, rect_height))
        else:
            pygame.draw.rect(self.button_surface, (0, 150, 0), (0, 0, rect_width, rect_height))

    def render(self, sc):
        self.button_surface.blit(self.text, self.text_rect)
        sc.blit(self.button_surface, (self.button_rect.x, self.button_rect.y))

        self.check_collidepoint(self.rect_width, self.rect_height)
