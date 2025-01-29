import pygame

import swordsman, archer, cavalry, dragon, castle
import enemys
import landscapes
import money

import start_game
from widgets import Button


class Screen:
    def __init__(self, size, main):
        self.gameplay = False
        self.back_to_menu = False
        self.choose_unit = None

        self.main = main

        self.size = self.width, self.height = size
        self.sc = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        self.board = Board(18, 10, self.size)

        self.button_start_game = Button('Начать игру', self.board.cell_size // 2, self.board.cell_size * 15,
                                        self.board.cell_size, coord_type="bottomleft")
        self.button_next_step = Button('Следующий ход', self.board.cell_size // 2, self.board.cell_size * 15,
                                       self.board.cell_size, coord_type="bottomleft")
        self.setting_button = Button('Настройки', self.board.cell_size // 2, self.board.cell_size * 4,
                                     self.board.cell_size, color=(255, 255, 0), dark_color=(50, 50, 50),
                                     coord_type="bottomleft")
        self.ref_button = Button('Справка', self.board.cell_size // 2, self.board.cell_size * 7, self.board.cell_size,
                                 color=(255, 255, 0), dark_color=(50, 50, 50), coord_type="bottomleft")
        self.back_button = Button('Назад', self.board.cell_size // 2, self.width / 20, self.board.cell_size,
                                  color=(200, 75, 75), dark_color=(150, 25, 25), coord_type="bottomleft")

        self.steps = 0
        self.score = 0
        self.money = 0
        self.progress = [1]
        self.choose_level = 1

        self.icon_swordsman = swordsman.Swordsman(self.board.cell_size * 1.4, 1 * (self.board.cell_size * 1.2),
                                                  self.board.cell_size * 1.2, swordsman.swordsmans)
        self.icon_archer = archer.Archer(self.board.cell_size * 1.4, 2 * (self.board.cell_size * 1.2),
                                         self.board.cell_size * 1.2, archer.archers)
        self.icon_cavalry = cavalry.Cavalry(self.board.cell_size * 1.4, 3 * (self.board.cell_size * 1.2),
                                            self.board.cell_size * 1.2, cavalry.cavalrys)
        self.icon_dragon = dragon.Dragon(self.board.cell_size * 1.4, 4 * (self.board.cell_size * 1.2),
                                         self.board.cell_size * 1.2, dragon.dragons)

        swordsman.stock = self.icon_swordsman.stock
        archer.stock = self.icon_archer.stock
        cavalry.stock = self.icon_cavalry.stock
        dragon.stock = self.icon_dragon.stock
        self.icon_money = money.Money(self.width - 100, 20, self.board.cell_size, money.moneys)

        self.choose_unit_surface = [
            pygame.surface.Surface((self.board.cell_size * 1.2, self.board.cell_size * 1.2)),
            [self.icon_swordsman.rect.x, self.icon_swordsman.rect.y]]

        self.cursor = pygame.image.load('images/different/cursor.PNG')
        self.cursor.set_colorkey((255, 255, 255))
        self.cursor = pygame.transform.scale(self.cursor, (20, 20))

    def get_click(self, mouse_pos, mouse_button):
        Board.get_click(self.board, mouse_pos, mouse_button, self)
        if not self.gameplay and self.button_start_game.check_click(mouse_pos):
            self.gameplay = True
        if not self.back_to_menu and self.back_button.check_click(mouse_pos):
            self.back_to_menu = True
            start_game.return_units()
            self.board.clear_board(self)
            self.main.start_screen.levels_menu.start()
        if self.setting_button.check_click(mouse_pos):
            self.main.start_screen.settings_screen.start()
        if self.ref_button.check_click(mouse_pos):
            self.main.start_screen.ref_screen.start()

    def render_cursor(self):
        pygame.mouse.set_visible(False)
        self.sc.blit(self.cursor, pygame.mouse.get_pos())

    def render(self):
        landscapes.landscapes.draw(self.sc)

        self.board.render(self.sc)

        self.choose_unit_surface[0].fill('green')
        self.choose_unit_surface[0].set_alpha(80)
        self.sc.blit(self.choose_unit_surface[0], self.choose_unit_surface[1])

        swordsman.swordsmans.draw(self.sc)
        archer.archers.draw(self.sc)
        cavalry.cavalrys.draw(self.sc)
        dragon.dragons.draw(self.sc)
        castle.castles.draw(self.sc)

        for unit in [swordsman, archer, cavalry, dragon]:
            index = [swordsman, archer, cavalry, dragon].index(unit) + 1
            unit.set_view_stock(self.sc, (round(self.board.cell_size * 0.9),
                                          index * (self.board.cell_size * 1.23) + round(self.board.cell_size / 2.6)),
                                round(self.board.cell_size / 1.4))

        enemys.swordsmans.draw(self.sc)
        enemys.archers.draw(self.sc)
        enemys.cavalrys.draw(self.sc)
        enemys.dragons.draw(self.sc)
        enemys.castles.draw(self.sc)

        self.back_button.render(self.sc)
        self.setting_button.render(self.sc)
        self.ref_button.render(self.sc)

        if not self.gameplay:
            self.button_start_game.render(self.sc)
            self.board.render_area(self.sc)
        else:
            self.button_next_step.render(self.sc)

        self.icon_money.render(self.sc, self.money)

    def choose_unit(self, mouse_pos):
        units = ['swordsman', 'archer', 'cavalry', 'dragon']
        if ((self.icon_swordsman.rect.left <= mouse_pos[0] <= self.icon_swordsman.rect.right and
             self.icon_swordsman.rect.top <= mouse_pos[1] <= self.icon_swordsman.rect.bottom) and
                self.icon_swordsman.stock > 0):
            self.choose_unit = units[0]
            self.choose_unit_surface[1] = [self.icon_swordsman.rect.x, self.icon_swordsman.rect.y]
        if ((self.icon_archer.rect.left <= mouse_pos[0] <= self.icon_archer.rect.right and
             self.icon_archer.rect.top <= mouse_pos[1] <= self.icon_archer.rect.bottom) and
                self.icon_archer.stock > 0):
            self.choose_unit = units[1]
            self.choose_unit_surface[1] = [self.icon_archer.rect.x, self.icon_archer.rect.y]
        if ((self.icon_cavalry.rect.left <= mouse_pos[0] <= self.icon_cavalry.rect.right and
             self.icon_cavalry.rect.top <= mouse_pos[1] <= self.icon_cavalry.rect.bottom)
                and self.icon_cavalry.stock > 0):
            self.choose_unit = units[2]
            self.choose_unit_surface[1] = [self.icon_cavalry.rect.x, self.icon_cavalry.rect.y]
        if ((self.icon_dragon.rect.left <= mouse_pos[0] <= self.icon_dragon.rect.right and
             self.icon_dragon.rect.top <= mouse_pos[1] <= self.icon_dragon.rect.bottom)
                and self.icon_dragon.stock > 0):
            self.choose_unit = units[3]
            self.choose_unit_surface[1] = [self.icon_dragon.rect.x, self.icon_dragon.rect.y]

        return self.choose_unit

    def reset_progress(self):
        self.steps = 0
        self.money = 0
        self.progress = [1]
        self.choose_level = 1
        self.board.clear_board(self)

        swordsman.stock = self.icon_swordsman.stock
        archer.stock = self.icon_archer.stock
        cavalry.stock = self.icon_cavalry.stock
        dragon.stock = self.icon_dragon.stock


class Board:
    def __init__(self, width, height, size):
        self.level = '1'
        self.choosen_unit = 'swordsman'

        self.width = width
        self.height = height

        self.cell_size = round(size[0] / 22)
        self.left = self.cell_size * 4
        self.top = round(self.cell_size * 1.5)

        self.board = [[0] * width for _ in range(height)]
        self.field = [[0] * width for _ in range(height)]

        self.allow_area = pygame.Surface((7 * self.cell_size, self.height * self.cell_size))
        self.allow_area.set_alpha(80)

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top

                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), 1)

    def render_area(self, screen):
        for i in range(len(self.board)):
            for j in range(7):
                if self.field[i][j] == 0 and self.board[i][j] == 0:
                    surface_coords_x = j * self.cell_size + self.left
                    surface_coords_y = i * self.cell_size + self.top
                    surface = pygame.surface.Surface((self.cell_size, self.cell_size))
                    surface.fill('yellow')
                    surface.set_alpha(80)
                    screen.blit(surface, (surface_coords_x, surface_coords_y))

    def set_map(self):
        self.set_team()
        self.set_enemys()
        self.set_landscapes()

    def set_team(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == (0, 4):
                    castle.add_start_castle(i * self.cell_size + self.left, j * self.cell_size + self.top,
                                            self.cell_size)
                    self.board[j][i], self.board[j][i + 1], self.board[j + 1][i], self.board[j + 1][i + 1] = 4, 4, 4, 4

    def set_enemys(self):
        with open(f'levels/{self.level}/enemys.txt', mode='rt', encoding='utf-8') as enemys_board:
            level_lst = [string.strip('\n').split(', ') for string in enemys_board]
            for i in range(len(level_lst)):
                for j in range(len(level_lst[i])):
                    x, y = j * self.cell_size + self.left, i * self.cell_size + self.top
                    if level_lst[i][j] == 's':
                        enemys.Enemy('swordsman', 'Рыцарь', x, y, 1, 1, 100, 20, 'images/enemy_images/swordsman.png',
                                     self.cell_size,
                                     enemys.swordsmans)
                        self.board[i][j] = 2
                    elif level_lst[i][j] == 'a':
                        enemys.Enemy('archer', 'Лучник', x, y, 1, 3, 40, 30, 'images/enemy_images/archer.png',
                                     self.cell_size,
                                     enemys.archers)
                        self.board[i][j] = 2
                    elif level_lst[i][j] == 'c':
                        enemys.Enemy('cavalry', 'Кавалерия', x, y, 3, 1, 70, 25, 'images/enemy_images/cavalry.png',
                                     self.cell_size,
                                     enemys.cavalrys)
                        self.board[i][j] = 2
                    elif level_lst[i][j] == 'd':
                        enemys.Enemy('dragon', 'Дракон', x, y, 4, 2, 150, 30, 'images/enemy_images/dragon.png',
                                     self.cell_size,
                                     enemys.dragons)
                        self.board[i][j] = 2
                    elif level_lst[i][j] == 'X':
                        enemys.Enemy('castle', 'Замок', x, y, 0, 0, 500, 0, 'images/enemy_images/castle.png',
                                     self.cell_size * 2,
                                     enemys.castles)
                        self.board[i][j], self.board[i + 1][j] = 3, 3
                        self.board[i][j + 1], self.board[i + 1][j + 1] = 3, 3

    def set_landscapes(self):
        with open(f'levels/{self.level}/field.txt', mode='rt', encoding='utf-8') as land:
            field_lst = [string.strip('\n').split(', ') for string in land]
            for i in range(len(field_lst)):
                for j in range(len(field_lst[i])):
                    x, y = j * self.cell_size + self.left, i * self.cell_size + self.top

                    landscapes.Landscape('grass', 'Трава', x, y, 'images/landscapes/grass.png', self.cell_size, 0, 0,
                                         landscapes.landscapes)

                    if field_lst[i][j] == 'm':
                        landscapes.Landscape('mountains', 'Гора', x, y, 'images/landscapes/mountains.png',
                                             self.cell_size,
                                             0, 'нельзя', landscapes.landscapes)
                        self.field[i][j] = 1
                    elif field_lst[i][j] == 'h':
                        landscapes.Landscape('hill', 'Холм', x, y, 'images/landscapes/hill.png', self.cell_size, 15, -1,
                                             landscapes.landscapes)
                        self.field[i][j] = 2
                    elif field_lst[i][j] == 'r':
                        landscapes.Landscape('river', 'Река', x, y, 'images/landscapes/river.png', self.cell_size, 0, 0,
                                             landscapes.landscapes)
                        self.field[i][j] = 3

    def get_cell(self, mouse_pos):
        xmax = self.left + self.width * self.cell_size
        ymax = self.top + self.height * self.cell_size
        if not (self.left <= mouse_pos[0] <= xmax and self.top <= mouse_pos[1] <= ymax):
            return -1, -1
        n_x = (mouse_pos[0] - self.left) // self.cell_size
        n_y = (mouse_pos[1] - self.top) // self.cell_size

        return n_x, n_y

    def on_click(self, cell_coords, mouse_button):
        x, y = cell_coords
        if mouse_button == 1:
            if x <= 6 and self.board[y][x] == 0 and self.field[y][x] == 0:
                if self.choosen_unit == 'swordsman' and swordsman.stock > 0:
                    swordsman.Swordsman(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                        swordsman.swordsmans)
                    swordsman.stock -= 1
                    self.board[y][x] = 1
                if self.choosen_unit == 'archer' and archer.stock > 0:
                    archer.Archer(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  archer.archers)
                    archer.stock -= 1
                    self.board[y][x] = 1

                if self.choosen_unit == 'cavalry' and cavalry.stock > 0:
                    cavalry.Cavalry(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                    cavalry.cavalrys)
                    cavalry.stock -= 1
                    self.board[y][x] = 1
                if self.choosen_unit == 'dragon' and dragon.stock > 0:
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

    def clear_board(self, screen):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.field = [[0] * self.width for _ in range(self.height)]

        swordsman.swordsmans.empty()
        archer.archers.empty()
        cavalry.cavalrys.empty()
        dragon.dragons.empty()
        castle.castles.empty()

        swordsman.swordsmans.add(screen.icon_swordsman)
        archer.archers.add(screen.icon_archer)
        cavalry.cavalrys.add(screen.icon_cavalry)
        dragon.dragons.add(screen.icon_dragon)

        enemys.swordsmans.empty()
        enemys.archers.empty()
        enemys.cavalrys.empty()
        enemys.dragons.empty()
        enemys.castles.empty()

        self.set_map()


class Window:
    def __init__(self, screen, size, main):
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.one_size = self.main_screen.board.cell_size
