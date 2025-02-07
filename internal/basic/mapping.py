import os

import pygame

import internal.basic.start_game as start_game
from internal.different import landscapes, money
from internal.different.global_vars import my_units_group, enemies_group, shop_group, landscape_group, UNIT_ARCHER, \
    UNIT_CAVALRY, UNIT_DRAGON, UNIT_SWORDSMAN, BOARD_EMPTY, BOARD_MY_UNIT, BOARD_ENEMY, BOARD_ENEMY_CASTLE, \
    BOARD_MY_CASTLE, FIELD_GRASS, FIELD_MOUNTAIN, FIELD_HILL, FIELD_RIVER
from internal.different.widgets import Button
from internal.units import swordsman, archer, castle, cavalry, dragon


class Screen:
    '''Создание класса основного экрана'''

    def __init__(self, size, main):
        '''Инициализация класса'''
        # задание переменных
        self.gameplay = False
        self.back_to_menu = False
        self.choose_unit = UNIT_SWORDSMAN

        self.main = main  # объект main

        self.size = self.width, self.height = size  # размер экрана
        self.sc = pygame.display.set_mode(self.size, pygame.FULLSCREEN)  # сам дисплей

        self.board = Board(18, 10, self.size)  # создание поля

        self.button_start_game = Button('Начать игру', self.board.cell_size // 2, self.board.cell_size * 15,
                                        self.board.cell_size, coord_type="bottomleft")  # кнопка начала игры
        self.button_next_step = Button('Следующий ход', self.board.cell_size // 2, self.board.cell_size * 15,
                                       self.board.cell_size, coord_type="bottomleft")  # кнопка след. хода
        self.setting_button = Button('Настройки', self.board.cell_size // 2, self.board.cell_size * 4,
                                     self.board.cell_size, color=(255, 255, 0), dark_color=(50, 50, 50),
                                     coord_type="bottomleft")  # кнопка настроек
        self.ref_button = Button('Справка', self.board.cell_size // 2, self.board.cell_size * 7, self.board.cell_size,
                                 color=(255, 255, 0), dark_color=(50, 50, 50),
                                 coord_type="bottomleft")  # кнопка справки
        self.back_button = Button('Назад', self.board.cell_size // 2, self.width / 20, self.board.cell_size,
                                  color=(200, 75, 75), dark_color=(150, 25, 25),
                                  coord_type="bottomleft")  # кнопка назад

        self.steps = 0  # кол-во шагов за 1 уровень

        self.score = 0  # очки
        self.best_score = 0  # лучший счёт
        self.summary_score = 0  # суммарные очки за все уровни

        # список умерших юнитов врага
        self.en_un_dead = {UNIT_SWORDSMAN: 0,
                           UNIT_ARCHER: 0,
                           UNIT_CAVALRY: 0,
                           UNIT_DRAGON: 0}

        # список умерших юнитов игрока
        self.my_un_dead = {UNIT_SWORDSMAN: 0,
                           UNIT_ARCHER: 0,
                           UNIT_CAVALRY: 0,
                           UNIT_DRAGON: 0}

        self.score_db = None  # DBO объект для доступа к таблице базы данных score
        self.money = 0  # монеты
        self.progress = {1}  # пройденные уровни
        self.choose_level = 1  # выбранный уровень (по умолчанию 1)

        self.icon_swordsman = swordsman.Swordsman(self.board.cell_size * 1.4, 1 * (self.board.cell_size * 1.2),
                                                  self.board.cell_size * 1.2, shop_group,
                                                  start_game.death_callback)  # иконка рыцаря (для выбора)
        self.icon_archer = archer.Archer(self.board.cell_size * 1.4, 2 * (self.board.cell_size * 1.2),
                                         self.board.cell_size * 1.2, shop_group,
                                         start_game.death_callback)  # иконка лучника (для выбора)
        self.icon_cavalry = cavalry.Cavalry(self.board.cell_size * 1.4, 3 * (self.board.cell_size * 1.2),
                                            self.board.cell_size * 1.2, shop_group,
                                            start_game.death_callback)  # иконка кавалерии (для выбора)
        self.icon_dragon = dragon.Dragon(self.board.cell_size * 1.4, 4 * (self.board.cell_size * 1.2),
                                         self.board.cell_size * 1.2, shop_group,
                                         start_game.death_callback)  # иконка дракона (для выбора)
        self.icon_money = money.Money(self.width - 100, 20, self.board.cell_size, money.moneys)  # иконка монет

        # запись кол-ва юнитов в инвентаре
        swordsman.stock = self.icon_swordsman.default_stock
        archer.stock = self.icon_archer.default_stock
        cavalry.stock = self.icon_cavalry.default_stock
        dragon.stock = self.icon_dragon.default_stock

        self.choose_unit_surface = None  # выбранный юнит (surface)
        for shop_unit in [self.icon_swordsman, self.icon_archer, self.icon_cavalry, self.icon_dragon]:
            if shop_unit.default_stock > 0:
                self.choose_unit_surface = [
                    pygame.surface.Surface((self.board.cell_size * 1.2, self.board.cell_size * 1.2)),
                    [shop_unit.rect.x, shop_unit.rect.y]]  # полотно выбранного юнита
                break

        # загрузка и настройка курсора
        self.cursor = pygame.image.load(os.path.join('images', 'different', 'cursor.jpg'))
        self.cursor.set_colorkey((255, 255, 255))
        self.cursor = pygame.transform.scale(self.cursor, (20, 20))

    def get_click(self, mouse_pos, mouse_button):
        '''Проверка на клик мышкой'''
        self.board.get_click(mouse_pos, mouse_button, self)
        if not self.gameplay and self.button_start_game.check_click(mouse_pos):  # при нажатии Начать игру
            self.gameplay = True
        if not self.back_to_menu and self.back_button.check_click(mouse_pos):  # при нажатии escape
            self.back_to_menu = True
            start_game.return_units()
            self.board.clear_board()  # очистка поля
            self.main.start_screen.levels_menu.start()
        if self.setting_button.check_click(mouse_pos):  # при нажатии настроек
            self.main.start_screen.settings_screen.start()
        if self.ref_button.check_click(mouse_pos):  # при нажатии справки
            self.main.start_screen.ref_screen.start()

    def render_cursor(self):
        '''Функция отображения курсора'''
        pygame.mouse.set_visible(False)  # отображение видимости обычного курсора
        self.sc.blit(self.cursor, pygame.mouse.get_pos())

    def render(self):
        '''Отображение ресурсов на экране'''
        landscape_group.draw(self.sc)  # отображение ландшафта

        self.board.render(self.sc)  # отображение доски

        if self.choose_unit_surface:  # отображение зеленого полотна выбранного юнита
            self.choose_unit_surface[0].fill('green')
            self.choose_unit_surface[0].set_alpha(80)
            self.sc.blit(self.choose_unit_surface[0], self.choose_unit_surface[1])

        shop_group.draw(self.sc)  # отображение иконок юнитов игрока

        for unit in [swordsman, archer, cavalry, dragon]:
            index = [swordsman, archer, cavalry, dragon].index(unit) + 1
            unit.set_view_stock(self.sc, (round(self.board.cell_size * 0.9),
                                          index * (self.board.cell_size * 1.23) + round(self.board.cell_size / 2.6)),
                                round(self.board.cell_size / 1.4))  # отображение кол-ва юнитов каждого типа в инвентаре

        enemies_group.draw(self.sc)  # отображение вражеских юнитов

        # отображение всех кнопок
        self.back_button.render(self.sc)
        self.setting_button.render(self.sc)
        self.ref_button.render(self.sc)

        if not self.gameplay:  # кнопка Начать игру
            self.button_start_game.render(self.sc)
            self.board.render_area(self.sc)
        else:  # кнопка Следующий ход
            self.button_next_step.render(self.sc)
            start_game.can_move(self)

        my_units_group.draw(self.sc)  # отображение юнитов игрока

        self.icon_money.render(self.sc, self.money)  # отображение монет

        # обновление анимаций групп спрайтов
        my_units_group.update()
        enemies_group.update()
        shop_group.update()

    def choose_unit(self, mouse_pos):
        '''Функция выбора юнитов'''
        if self.icon_swordsman.rect.collidepoint(mouse_pos) and swordsman.stock > 0:  # выбор рыцаря
            self.choose_unit = UNIT_SWORDSMAN
            self.choose_unit_surface[1] = [self.icon_swordsman.rect.x, self.icon_swordsman.rect.y]
        if self.icon_archer.rect.collidepoint(mouse_pos) and archer.stock > 0:  # выбор лучника
            self.choose_unit = UNIT_ARCHER
            self.choose_unit_surface[1] = [self.icon_archer.rect.x, self.icon_archer.rect.y]
        if self.icon_cavalry.rect.collidepoint(mouse_pos) and cavalry.stock > 0:  # выбор кавалерии
            self.choose_unit = UNIT_CAVALRY
            self.choose_unit_surface[1] = [self.icon_cavalry.rect.x, self.icon_cavalry.rect.y]
        if self.icon_dragon.rect.collidepoint(mouse_pos) and dragon.stock > 0:  # выбор дракона
            self.choose_unit = UNIT_DRAGON
            self.choose_unit_surface[1] = [self.icon_dragon.rect.x, self.icon_dragon.rect.y]

        return self.choose_unit

    def reset_progress(self):
        '''Сброс прогресса (reset)'''
        self.steps = 0
        self.score = 0
        self.money = 0
        self.progress = {1}
        self.choose_level = 1

        self.board.clear_board()  # очистка доски
        self.main.start_screen.levels_menu.lst_buttons = [self.main.start_screen.levels_menu.back_button, ]

        # возвращение базового кол-ва юнитов
        swordsman.stock = self.icon_swordsman.default_stock
        archer.stock = self.icon_archer.default_stock
        cavalry.stock = self.icon_cavalry.default_stock
        dragon.stock = self.icon_dragon.default_stock


class Board:
    '''Создание класса игрового поля (board)'''

    def __init__(self, width, height, size):
        '''Инициализация класса'''
        self.level = '1'  # уровень по умолчанию
        self.choosen_unit = UNIT_SWORDSMAN  # юнит по умолчанию

        self.width = width  # ширина
        self.height = height  # высота

        self.cell_size = round(size[0] / 22)  # размер клетки
        self.left = self.cell_size * 4  # размер отступа слева
        self.top = round(self.cell_size * 1.5)  # размер отступа сверху

        self.board = [[BOARD_EMPTY] * width for _ in range(height)]  # создание двумерного списка поля юнитов
        self.field = [[FIELD_GRASS] * width for _ in range(height)]  # создание двумерного списка поля ландшафтов

        self.allow_area = pygame.Surface((7 * self.cell_size, self.height * self.cell_size))
        self.allow_area.set_alpha(80)

    def render(self, screen):
        '''Рендер сетки поля'''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top

                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), 1)

    def render_area(self, screen):
        '''Отображение допустимого расстояния размещения юнитов от башни'''
        for i in range(len(self.board)):
            for j in range(5):
                if self.field[i][j] == FIELD_GRASS and self.board[i][j] == BOARD_EMPTY:
                    surface_coords_x = j * self.cell_size + self.left
                    surface_coords_y = i * self.cell_size + self.top
                    surface = pygame.surface.Surface((self.cell_size, self.cell_size))
                    surface.fill('yellow')
                    surface.set_alpha(80)
                    screen.blit(surface, (surface_coords_x, surface_coords_y))

    def set_map(self):
        '''Установка карты'''
        self.set_team()
        self.set_enemys()
        self.set_landscapes()

    def set_team(self):
        '''Установка юнитов (башни)'''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == (0, 4):
                    castle.Castle(i * self.cell_size + self.left, j * self.cell_size + self.top, self.cell_size * 2,
                                  my_units_group, start_game.death_callback)
                    self.board[j][i], self.board[j][i + 1] = [BOARD_MY_CASTLE] * 2
                    self.board[j + 1][i], self.board[j + 1][i + 1] = [BOARD_MY_CASTLE] * 2

    def set_enemys(self):
        '''Установка врагов'''
        with open(os.path.join('levels', str(self.level), 'enemys.txt'), mode='rt', encoding='utf-8') as enemys_board:
            level_lst = [string.strip('\n').split(', ') for string in enemys_board]  # получение юнитов из файлов
            for i in range(len(level_lst)):
                for j in range(len(level_lst[i])):
                    x, y = j * self.cell_size + self.left, i * self.cell_size + self.top
                    if level_lst[i][j] == 's':  # устновка рыцарей
                        swordsman.Swordsman(x, y, self.cell_size, enemies_group,
                                            start_game.death_callback, mirror_animation=True)
                        self.board[i][j] = BOARD_ENEMY
                    elif level_lst[i][j] == 'a':  # установка лучников
                        archer.Archer(x, y, self.cell_size, enemies_group,
                                      start_game.death_callback, mirror_animation=True)
                        self.board[i][j] = BOARD_ENEMY
                    elif level_lst[i][j] == 'c':  # установка кавалерии
                        cavalry.Cavalry(x, y, self.cell_size, enemies_group,
                                        start_game.death_callback, mirror_animation=True)
                        self.board[i][j] = BOARD_ENEMY
                    elif level_lst[i][j] == 'd':  # установка драконов
                        dragon.Dragon(x, y, self.cell_size, enemies_group,
                                      start_game.death_callback, mirror_animation=True)
                        self.board[i][j] = BOARD_ENEMY
                    elif level_lst[i][j] == 'X':  # установка башни (башен)
                        castle.Castle(x, y, self.cell_size * 2, enemies_group, start_game.death_callback)
                        self.board[i][j], self.board[i + 1][j] = [BOARD_ENEMY_CASTLE] * 2
                        self.board[i][j + 1], self.board[i + 1][j + 1] = [BOARD_ENEMY_CASTLE] * 2

    def set_landscapes(self):
        '''Установка ландшафтов'''
        with open(os.path.join('levels', str(self.level), 'field.txt'), mode='rt', encoding='utf-8') as land:
            field_lst = [string.strip('\n').split(', ') for string in land]
            for i in range(len(field_lst)):
                for j in range(len(field_lst[i])):
                    x, y = self.get_cell_coords((j, i))

                    if field_lst[i][j] in ['m', 'h']:  # если наземные
                        landscapes.Landscape('grass', 'Трава', x, y,
                                             os.path.join('images', 'landscapes', 'grass.jpg'),
                                             self.cell_size, 0, 0, landscape_group)  # установка травы
                        if field_lst[i][j] == 'm':  # установка гор
                            landscapes.Landscape('mountains', 'Гора', x, y,
                                                 os.path.join('images', 'landscapes', 'mountains.jpg'),
                                                 self.cell_size, 0, 'нельзя', landscape_group)
                            self.field[i][j] = FIELD_MOUNTAIN
                        elif field_lst[i][j] == 'h':  # установка холмов
                            landscapes.Landscape('hill', 'Холм', x, y,
                                                 os.path.join('images', 'landscapes', 'hill.jpg'),
                                                 self.cell_size, 15, -1, landscape_group)
                            self.field[i][j] = FIELD_HILL

                    elif field_lst[i][j] in ['r']:  # если не наземные
                        if field_lst[i][j] == 'r':  # если река
                            landscapes.Landscape('river', 'Река', x, y,
                                                 os.path.join('images', 'landscapes', 'river.jpg'),
                                                 self.cell_size, 0, 0, landscape_group)
                            self.field[i][j] = FIELD_RIVER
                    else:  # иначе установка травы
                        landscapes.Landscape('grass', 'Трава', x, y,
                                             os.path.join('images', 'landscapes', 'grass.jpg'),
                                             self.cell_size, 0, 0, landscape_group)

    def get_cell(self, mouse_pos):
        '''Функция получения клетки по координатам мышки'''
        xmax = self.left + self.width * self.cell_size
        ymax = self.top + self.height * self.cell_size
        if not (self.left <= mouse_pos[0] <= xmax and self.top <= mouse_pos[1] <= ymax):
            return -1, -1
        n_x = (mouse_pos[0] - self.left) // self.cell_size
        n_y = (mouse_pos[1] - self.top) // self.cell_size

        return n_x, n_y

    def get_cell_coords(self, cell):
        '''Функция получения координат по клетке'''
        x, y = cell
        return x * self.cell_size + self.left, y * self.cell_size + self.top

    def on_click(self, cell_coords, mouse_button):
        '''Функция размещения/возвращения юнитов на поле/с поля'''
        x, y = cell_coords
        if mouse_button == 1:  # при ЛКМ
            if x <= 4 and self.board[y][x] == BOARD_EMPTY and self.field[y][x] == FIELD_GRASS:
                if self.choosen_unit == UNIT_SWORDSMAN and swordsman.stock > 0:  # рыцарь
                    swordsman.Swordsman(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                        my_units_group, start_game.death_callback)
                    swordsman.stock -= 1
                    self.board[y][x] = BOARD_MY_UNIT

                if self.choosen_unit == UNIT_ARCHER and archer.stock > 0:  # лучник
                    archer.Archer(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  my_units_group, start_game.death_callback)
                    archer.stock -= 1
                    self.board[y][x] = BOARD_MY_UNIT

                if self.choosen_unit == UNIT_CAVALRY and cavalry.stock > 0:  # кавалерия
                    cavalry.Cavalry(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                    my_units_group, start_game.death_callback)
                    cavalry.stock -= 1
                    self.board[y][x] = BOARD_MY_UNIT

                if self.choosen_unit == UNIT_DRAGON and dragon.stock > 0:  # дракон
                    dragon.Dragon(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  my_units_group, start_game.death_callback)
                    dragon.stock -= 1
                    self.board[y][x] = BOARD_MY_UNIT

        if mouse_button == 3:  # при ПКМ - возврат юнита в инвентарь
            if self.board[y][x] == BOARD_MY_UNIT:
                coords = x * self.cell_size + self.left, y * self.cell_size + self.top

                dct = {UNIT_SWORDSMAN: swordsman,
                       UNIT_ARCHER: archer,
                       UNIT_CAVALRY: cavalry,
                       UNIT_DRAGON: dragon}
                for unit in my_units_group:  # возврат юнита
                    if unit.rect.collidepoint(coords):
                        my_units_group.remove(unit)
                        dct[unit.name].stock += 1

                self.board[y][x] = BOARD_EMPTY

    def get_click(self, mouse_pos, mouse_button, screen):
        '''Функция получения клетки и проверка на размещение юнита'''
        cell = self.get_cell(mouse_pos)
        self.choosen_unit = Screen.choose_unit(screen, mouse_pos)
        if cell[0] >= 0 and cell[1] >= 0:
            self.on_click(cell, mouse_button)

    def clear_board(self):
        '''Функция очистки поля'''
        self.board = [[BOARD_EMPTY] * self.width for _ in range(self.height)]
        self.field = [[FIELD_GRASS] * self.width for _ in range(self.height)]

        my_units_group.empty()
        enemies_group.empty()
        landscape_group.empty()

        self.set_map()
