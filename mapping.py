import pygame

import swordsman
import castle
import cavalry
import archer
import dragon
import landscapes

import enemys


class Screen:
    def __init__(self, size):
        self.sc = pygame.display.set_mode(size)
        self.choose_unit = None
        self.board = Board(18, 10)
        self.button_start_game = Button('Начать игру', 38, 200, 26, 1100, 700)
        self.icon_swordsman = swordsman.Swordsman(125, 25, 80, swordsman.swordsmans)
        self.icon_archer = archer.Archer(125, 125, 80, archer.archers)
        self.icon_cavalry = cavalry.Cavalry(125, 225, 80, cavalry.cavalrys)
        self.icon_dragon = dragon.Dragon(125, 325, 80, dragon.dragons)

    def choose_unit(self, mouse_pos):
        if (self.icon_swordsman.rect.left <= mouse_pos[0] <= self.icon_swordsman.rect.right and
                self.icon_swordsman.rect.top <= mouse_pos[1] <= self.icon_swordsman.rect.bottom):
            self.choose_unit = 'swordsman'
        if (self.icon_archer.rect.left <= mouse_pos[0] <= self.icon_archer.rect.right and
                self.icon_archer.rect.top <= mouse_pos[1] <= self.icon_archer.rect.bottom):
            self.choose_unit = 'archer'
        if (self.icon_cavalry.rect.left <= mouse_pos[0] <= self.icon_cavalry.rect.right and
                self.icon_cavalry.rect.top <= mouse_pos[1] <= self.icon_cavalry.rect.bottom):
            self.choose_unit = 'cavalry'
        if (self.icon_dragon.rect.left <= mouse_pos[0] <= self.icon_dragon.rect.right and
                self.icon_dragon.rect.top <= mouse_pos[1] <= self.icon_dragon.rect.bottom):
            self.choose_unit = 'dragon'

        return self.choose_unit

    def render(self):
        landscapes.grasses.draw(self.sc)
        self.board.render(self.sc)
        castle.castles.draw(self.sc)
        swordsman.swordsmans.draw(self.sc)
        swordsman.set_view_stock(self.sc, (50, 50))
        archer.archers.draw(self.sc)
        archer.set_view_stock(self.sc, (50, 150))
        cavalry.cavalrys.draw(self.sc)
        cavalry.set_view_stock(self.sc, (50, 250))
        dragon.dragons.draw(self.sc)
        dragon.set_view_stock(self.sc, (50, 350))

        enemys.swordsmans.draw(self.sc)
        enemys.archers.draw(self.sc)
        enemys.cavalrys.draw(self.sc)
        enemys.dragons.draw(self.sc)

        self.button_start_game.render(self.sc)

    def get_click(self, mouse_pos, mouse_button):
        Board.get_click(self.board, mouse_pos, mouse_button, self)
        if not self.board.gameplay and (
                self.button_start_game.button_rect.left <= mouse_pos[0] <= self.button_start_game.button_rect.right
                and
                self.button_start_game.button_rect.top <= mouse_pos[1] <= self.button_start_game.button_rect.bottom):
            self.board.gameplay = True


class Board:
    def __init__(self, width, height):
        self.gameplay = False
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

        with (open('levels/1.txt', mode='rt', encoding='utf-8') as level):
            level_lst = [string.strip('\n').split(', ') for string in level]
            for i in range(len(level_lst)):
                for j in range(len(level_lst[i])):
                    x, y = j * self.cell_size + self.left, i * self.cell_size + self.top
                    if level_lst[i][j] == 's':
                        enemys.Enemy(x, y, 1, 1, 'images/swordsman.jpeg', self.cell_size, enemys.swordsmans)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'a':
                        enemys.Enemy(x, y, 1, 4, 'images/archer.jpeg', self.cell_size, enemys.swordsmans)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'c':
                        enemys.Enemy(x, y, 3, 1, 'images/cavalry.jpeg', self.cell_size, enemys.swordsmans)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'd':
                        enemys.Enemy(x, y, 4, 3, 'images/dragon.jpeg', self.cell_size, enemys.swordsmans)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'X':
                        enemys.Enemy(x, y, 0, 0, 'images/castle.jpeg', self.cell_size * 2, enemys.swordsmans)
                        self.board[i][j], self.board[i + 1][j] = 2, 2
                        self.board[i][j + 1], self.board[i + 1][j + 1] = 2, 2

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
            if x <= 5:
                if self.choosen_unit == 'swordsman' and self.board[y][x] == 0 and swordsman.stock > 0:
                    swordsman.Swordsman(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                        swordsman.swordsmans)
                    swordsman.stock -= 1
                    self.board[y][x] = 1
                if self.choosen_unit == 'archer' and self.board[y][x] == 0 and archer.stock > 0:
                    archer.Archer(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  archer.archers)
                    archer.stock -= 1
                    self.board[y][x] = 1

                if self.choosen_unit == 'cavalry' and self.board[y][x] == 0 and cavalry.stock > 0:
                    cavalry.Cavalry(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                    cavalry.cavalrys)
                    cavalry.stock -= 1
                    self.board[y][x] = 1
                if self.choosen_unit == 'dragon' and self.board[y][x] == 0 and dragon.stock > 0:
                    dragon.Dragon(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  dragon.dragons)
                    dragon.stock -= 1
                    self.board[y][x] = 1

        if mouse_button == 3:
            if self.board[y][x] == 1:
                coords = x * self.cell_size + self.left, y * self.cell_size + self.top

                for sword in swordsman.swordsmans:
                    if (sword.rect.x, sword.rect.y) == coords:
                        swordsman.swordsmans.remove(sword)
                        swordsman.stock += 1

                for arc in archer.archers:
                    if (arc.rect.x, arc.rect.y) == coords:
                        archer.archers.remove(arc)
                        archer.stock += 1

                for cav in cavalry.cavalrys:
                    if (cav.rect.x, cav.rect.y) == coords:
                        cavalry.cavalrys.remove(cav)
                        cavalry.stock += 1

                for drg in dragon.dragons:
                    if (drg.rect.x, drg.rect.y) == coords:
                        dragon.dragons.remove(drg)
                        dragon.stock += 1

                self.board[y][x] = 0

    def get_click(self, mouse_pos, mouse_button, screen):
        cell = self.get_cell(mouse_pos)
        self.choosen_unit = Screen.choose_unit(screen, mouse_pos)
        if cell[0] >= 0 and cell[1] >= 0:
            self.on_click(cell, mouse_button)


class Button:
    def __init__(self, text, size_font, surface_x, surface_y, rect_x, rect_y):
        self.font = pygame.font.Font(None, size_font)
        self.button_surface = pygame.Surface((surface_x, surface_y))
        self.text = self.font.render(text, True, (255, 255, 255))
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
