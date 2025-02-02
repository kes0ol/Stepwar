import sys

import pygame

import mapping
import swordsman, cavalry, castle, archer, dragon, landscapes

from widgets import Button, View


class Reference_window(mapping.Window):
    '''Создание класса первого окна справки'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main)
        self.ref_screen = Description(self.main_screen, self.size, self.main)  # создание второго окна
        self.next_page_button = Button('->', 200, self.width - 80, self.height - 80,
                                       color=(100, 0, 0), dark_color=(50, 0, 0))  # создание кнопки на след. страницу
        self.back_button = Button('Назад', 80, 120, self.height - 70, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))  # создание кнопки Назад
        self.lst_buttons = [self.back_button, self.next_page_button]  # список кнопок

        self.control_view = View('Управление', self.one_size, self.width // 2, self.one_size,
                                 color=(100, 0, 0))  # создание надписи

        t = ('''Выход на предыдущий экран (назад): Esc\nВыбор юнита в инвентаре: 1/2/3/4\nСледующий ход: Space\n\nВ главном меню:
        Список уровней: 1
        Магазин: 2
        Настройки: 3
        Справка: 4\n\nВ списке уровней:
        Первый уровень: 1
        Второй уровень: 2
        Третий уровень: 3''')  # задание текста справки

        self.lst = t.split('\n')

        self.fon = pygame.image.load('images/backgrounds/ref_background.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

    def parse_text(self, text, width):
        '''Функция парсинга текста (при надобности)'''
        lst = text.split()
        res = []
        w = width
        st = ''
        while len(lst) > 1:
            while w > 0 and len(lst) > 1:
                if len(lst[0]) > 0:
                    st += lst[0] + ' '
                    lst = lst[1:]
                    w -= len(lst[0])
                else:
                    break
            w = width
            res.append(st)
            st = ''
        return res

    def check_click(self, mouse_pos, lst):
        '''Функция проверка клика мышки'''
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.next_page_button:  # при нажатии на кнопку следующей страницы
                    self.ref_screen.start()
                if button == self.back_button:  # при нажатии на кнопку Назад
                    self.running = False

    def render(self):
        '''Рендер содержимого страницы'''
        y = self.one_size
        self.main_screen.sc.blit(self.fon, (0, 0))
        for i in self.lst:
            font = pygame.font.Font(None, round(self.one_size / 1.7))
            text = font.render(i, True, 'black')
            self.main_screen.sc.blit(text, (self.one_size, self.one_size + y))
            y += round(self.one_size / 1.7)
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.control_view.render(self.main_screen.sc)
        self.main_screen.render_cursor()

    def start(self):
        '''Функция старта основного цикла'''
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:  # старт цикла
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # проверка выхода
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # при нажатии на клавиши
                    if event.key == pygame.K_ESCAPE:  # если нажат escape
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # при нажатии мышкой
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()


class Description(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.back_button = Button('<-', round(self.one_size * 2.4), self.one_size,
                                  self.height - self.one_size, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.swordsman_button = Button('Рыцарь', round(self.one_size * 1.2), self.one_size * 3,
                                       self.one_size, color=(100, 0, 0),
                                       dark_color=(50, 0, 0))
        self.archer_button = Button('Лучник', round(self.one_size * 1.2), self.one_size * 3,
                                    round(self.one_size * 2.5), color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.cavalry_button = Button('Кавалерия', round(self.one_size * 1.2), self.one_size * 3,
                                     self.one_size * 4, color=(100, 0, 0),
                                     dark_color=(50, 0, 0))
        self.dragon_button = Button('Дракон', round(self.one_size * 1.2), self.one_size * 3,
                                    round(self.one_size * 5.5), color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.castle_button = Button('Замок', round(self.one_size * 1.2), self.one_size * 3,
                                    self.one_size * 7, color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.grass_button = Button('Трава', round(self.one_size * 1.2), self.one_size * 8,
                                   self.one_size, color=(100, 0, 0),
                                   dark_color=(50, 0, 0))
        self.rock_button = Button('Гора', round(self.one_size * 1.2), self.one_size * 8,
                                  round(self.one_size * 2.5), color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.hill_button = Button('Холм', round(self.one_size * 1.2), self.one_size * 8,
                                  self.one_size * 4, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.river_button = Button('Река', round(self.one_size * 1.2), self.one_size * 8,
                                   round(self.one_size * 5.5), color=(100, 0, 0),
                                   dark_color=(50, 0, 0))

        self.icons_units = pygame.sprite.Group()

        self.lst_buttons = [self.back_button, self.swordsman_button, self.archer_button, self.cavalry_button,
                            self.dragon_button, self.castle_button, self.grass_button, self.rock_button,
                            self.hill_button, self.river_button]

        self.dct_units = {self.swordsman_button: swordsman.Swordsman,
                          self.archer_button: archer.Archer,
                          self.cavalry_button: cavalry.Cavalry,
                          self.dragon_button: dragon.Dragon,
                          self.castle_button: castle.Castle}

        self.dct_lands = {self.grass_button: ('grass', 'Трава', self.one_size * 16.1, self.one_size * 4.1,
                                              'images/landscapes/grass.png', self.one_size * 4, 0, 0,
                                              self.icons_units),
                          self.rock_button: ('mountains', 'Гора', self.one_size * 16.1, self.one_size * 4.1,
                                             'images/landscapes/mountains.png', self.one_size * 4, 0, 'нельзя',
                                             self.icons_units),
                          self.hill_button: ('hill', 'Холм', self.one_size * 16.1, self.one_size * 4.1,
                                             'images/landscapes/hill.png', self.one_size * 4, 15, -1,
                                             self.icons_units),
                          self.river_button: ('river', 'Река', self.one_size * 16.1, self.one_size * 4.1,
                                              'images/landscapes/river.png', self.one_size * 4, 0, 'Частично',
                                              self.icons_units)}

        self.stats = []

        self.fon = pygame.image.load('images/backgrounds/ref_background.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

    def check_click(self, mouse_pos, lst):
        self.icons_units.empty()
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                elif button in self.dct_units.keys():
                    self.icon_unit = self.dct_units[button](self.one_size * 16.1, self.one_size * 4.1,
                                                            self.one_size * 4, self.icons_units)
                    self.stats = [f'Тип юнита: {self.icon_unit.title}',
                                  f'Здоровье: {self.icon_unit.hp}',
                                  f'Урон: {self.icon_unit.damage}',
                                  f'Передвижение: {self.icon_unit.step}',
                                  f'Дистанция атаки: {self.icon_unit.distance_attack}']
                elif button in self.dct_lands.keys():
                    self.icon_land = landscapes.Landscape(*self.dct_lands[button])
                    self.stats = [
                        f'Ландшафт: {self.icon_land.title}',
                        f'Доп. урон: {self.icon_land.damage}',
                        f'Передвижение: {self.icon_land.move}']

    def render(self):
        y = 50
        f = pygame.font.Font(None, round(self.one_size * 1.3))
        t = f.render('Информация', True, 'black')

        self.main_screen.sc.blit(self.fon, (0, 0))
        if len(self.icons_units):
            pygame.draw.rect(self.main_screen.sc, (66, 44, 33), (self.one_size * 10, self.one_size,
                                                                 self.one_size * 11, self.one_size * 9), 8)
            pygame.draw.rect(self.main_screen.sc, (0, 0, 0), (self.one_size * 16, self.one_size * 4,
                                                              self.one_size * 4.2, self.one_size * 4.2), 8)
            for i in reversed(self.stats):
                font = pygame.font.Font(None, round(self.one_size * 0.5))
                text = font.render(i, True, 'black')
                self.main_screen.sc.blit(text, (self.one_size * 11, self.one_size * 8 - y))
                y += 50

            self.main_screen.sc.blit(t, (self.one_size * 11, self.one_size * 2))
            self.icons_units.draw(self.main_screen.sc)

        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.render_cursor()

    def start(self):
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
