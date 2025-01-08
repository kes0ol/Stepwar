import pygame

import enemys
import swordsman
import castle
import cavalry
import archer
import dragon
import landscapes

from widgets import Button


class Screen:
    def __init__(self, size):
        self.gameplay = False
        self.back_to_menu = False
        self.choose_unit = None

        self.size = width, height = size
        self.sc = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        self.board = Board(18, 10, self.size)
        self.button_start_game = Button('Начать игру', 38, 20, height - 20, coord_type="bottomleft")
        self.button_next_step = Button('Следующий ход', 38, 120, height - 20, coord_type="midbottom")
        self.back_button = Button('Вернуться в главное меню', 40, width - 20, height - 20, color=(200, 75, 75),
                                  dark_color=(150, 25, 25), coord_type="bottomright")

        self.icon_swordsman = swordsman.Swordsman(125, 25, self.board.cell_size * 1.5, swordsman.swordsmans)
        swordsman.stock = self.icon_swordsman.stock
        self.icon_archer = archer.Archer(125, 125, self.board.cell_size * 1.5, archer.archers)
        archer.stock = self.icon_archer.stock
        self.icon_cavalry = cavalry.Cavalry(125, 225, self.board.cell_size * 1.5, cavalry.cavalrys)
        cavalry.stock = self.icon_cavalry.stock
        self.icon_dragon = dragon.Dragon(125, 325, self.board.cell_size * 1.5, dragon.dragons)
        dragon.stock = self.icon_dragon.stock

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

        swordsman.swordsmans.draw(self.sc)
        swordsman.set_view_stock(self.sc, (50, 50))
        archer.archers.draw(self.sc)
        archer.set_view_stock(self.sc, (50, 150))
        cavalry.cavalrys.draw(self.sc)
        cavalry.set_view_stock(self.sc, (50, 250))
        dragon.dragons.draw(self.sc)
        dragon.set_view_stock(self.sc, (50, 350))
        castle.castles.draw(self.sc)

        enemys.swordsmans.draw(self.sc)
        enemys.archers.draw(self.sc)
        enemys.cavalrys.draw(self.sc)
        enemys.dragons.draw(self.sc)
        enemys.castles.draw(self.sc)

        self.back_button.render(self.sc)

        if not self.gameplay:
            self.button_start_game.render(self.sc)
        else:
            self.button_next_step.render(self.sc)

    def get_click(self, mouse_pos, mouse_button):
        Board.get_click(self.board, mouse_pos, mouse_button, self)
        if not self.gameplay and self.button_start_game.check_click(mouse_pos):
            self.gameplay = True
        if not self.back_to_menu and self.back_button.check_click(mouse_pos):
            self.back_to_menu = True
            self.board.clear_board(self.icon_swordsman, self.icon_archer, self.icon_cavalry, self.icon_dragon)


class Board:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height

        self.cell_size = round(size[0] / 22)
        self.left = self.cell_size * 4
        self.top = self.cell_size // 2

        self.board = [[0] * width for _ in range(height)]
        self.landscape = [[0] * width for _ in range(height)]

        self.set_team()
        self.set_enemys()
        self.set_landscapes()

    def set_enemys(self):
        with open('levels/1.txt', mode='rt', encoding='utf-8') as level:
            level_lst = [string.strip('\n').split(', ') for string in level]
            for i in range(len(level_lst)):
                for j in range(len(level_lst[i])):
                    x, y = j * self.cell_size + self.left, i * self.cell_size + self.top
                    if level_lst[i][j] == 's':
                        enemys.Enemy('Рыцарь', x, y, 1, 1, 100, 20, 'images/enemy_images/swordsman2.png',
                                     self.cell_size,
                                     enemys.swordsmans)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'a':
                        enemys.Enemy('Лучник', x, y, 1, 3, 40, 30, 'images/enemy_images/archer.png',
                                     self.cell_size,
                                     enemys.archers)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'c':
                        enemys.Enemy('Кавалерия', x, y, 3, 1, 70, 25, 'images/enemy_images/cavalry.png',
                                     self.cell_size,
                                     enemys.cavalrys)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'd':
                        enemys.Enemy('Дракон', x, y, 4, 2, 150, 30, 'images/enemy_images/dragon.png',
                                     self.cell_size,
                                     enemys.dragons)
                        self.board[i][j] = 2
                    if level_lst[i][j] == 'X':
                        enemys.Enemy('Замок', x, y, 0, 0, 500, 0, 'images/enemy_images/castle.jpg',
                                     self.cell_size * 2,
                                     enemys.castles)
                        self.board[i][j], self.board[i + 1][j] = 3, 3
                        self.board[i][j + 1], self.board[i + 1][j + 1] = 3, 3

    def set_team(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == (0, 4):
                    castle.add_start_castle(i * self.cell_size + self.left, j * self.cell_size + self.top,
                                            self.cell_size)
                    self.board[j][i], self.board[j][i + 1], self.board[j + 1][i], self.board[j + 1][i + 1] = 4, 4, 4, 4

    def set_landscapes(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top

                if self.landscape[i][j] == 0:
                    landscapes.Grass(x, y, self.cell_size, landscapes.grasses)
                    self.landscape[i][j] = 1

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

    def on_click(self, cell_coords, mouse_button):
        x, y = cell_coords
        if mouse_button == 1:
            if x <= 6:
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

    def clear_board(self, icon_swordsman, icon_archer, icon_cavalry, icon_dragon):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.landscape = [[0] * self.width for _ in range(self.height)]

        swordsman.swordsmans.empty()
        swordsman.swordsmans.add(icon_swordsman)
        swordsman.stock = icon_swordsman.stock
        archer.archers.empty()
        archer.archers.add(icon_archer)
        archer.stock = icon_archer.stock
        cavalry.cavalrys.empty()
        cavalry.cavalrys.add(icon_cavalry)
        cavalry.stock = icon_cavalry.stock
        dragon.dragons.empty()
        dragon.dragons.add(icon_dragon)
        dragon.stock = icon_dragon.stock

        enemys.swordsmans.empty()
        enemys.archers.empty()
        enemys.cavalrys.empty()
        enemys.dragons.empty()
        enemys.castles.empty()

        self.set_team()
        self.set_enemys()
        self.set_landscapes()
