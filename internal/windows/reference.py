import os

import pygame

from internal.different import landscapes
from internal.different.widgets import Button, View
from internal.units import archer, castle, swordsman, dragon, cavalry
from internal.windows import window


class Reference_window(window.Window):
    '''Создание класса первого окна справки'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'ref_background.jpg'))

        self.next_page_button = Button('->', round(self.s * 2.4), self.width - 80, self.height - 80,
                                       color=(100, 0, 0), dark_color=(50, 0, 0))  # создание кнопки на след. страницу
        self.back_button = Button('Назад', 80, 120, self.height - 70, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))  # создание кнопки Назад
        self.control_view = View('Управление', self.s, self.width // 2, self.s,
                                 color=(100, 0, 0))  # создание надписи

        window.Window.set_lists(self, [self.back_button, self.next_page_button], [self.control_view, ])

        self.ref_screen = Description(self.main_screen, self.size, self.main)  # создание второго окна

        t1 = ('''Выход на предыдущий экран (назад): Esc\nВыбор юнита в инвентаре: 1/2/3/4\nСледующий ход: Space/Enter\n\nВ главном меню:
        Список уровней: 1
        Магазин: 2
        Настройки: 3
        Справка: 4
        Счёт: 5\n\nВ уровне:
        Передвижение юнитом: ЛКМ
        Атаковать юнитом: ПКМ''')

        t2 = ('''В списке уровней:
        Первый уровень: 1
        Второй уровень: 2
        Третий уровень: 3\n\nВ настройках:
        Понизить громкость - минус(-)
        Повысить громкость - равно(=)\n\nВ справке:
        След. страница: стрелка влево
        Пред. страница: стрелка вправо\n\nВ счёте:
        След. страница: стрелка влево
        Пред. страница: стрелка вправо''')

        self.lst = [text.split('\n') for text in (t1, t2)]

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))

    def check_click(self, mouse_pos, lst):
        '''Функция проверка клика мышки'''
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.next_page_button:  # при нажатии на кнопку следующей страницы
                    self.ref_screen.start()
                if button == self.back_button:  # при нажатии на кнопку Назад
                    self.running = False

    @window.Window.render_decorator
    def render(self):
        '''Рендер содержимого страницы'''
        y = self.s

        for index in range(len(self.lst)):
            for i in self.lst[index]:
                font = pygame.font.Font(None, round(self.s / 1.7))
                text = font.render(i, True, 'black')
                self.screen.blit(text, (self.width // 2 * index + self.s, self.s + y))
                y += round(self.s / 1.7)
            y = self.s

    @window.Window.start_decoration
    def start(self, event):
        '''Функция старта основного цикла'''
        if event.type == pygame.KEYDOWN:  # при нажатии на клавиши
            if event.key == pygame.K_ESCAPE:  # если нажат escape
                self.running = False
            if event.key == pygame.K_RIGHT:
                self.ref_screen.start()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)


class Description(window.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main, ('images', 'backgrounds', 'ref_background.jpg'))
        self.back_button = Button('<-', round(self.s * 2.4), self.s,
                                  self.height - self.s, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.swordsman_button = Button('Рыцарь', round(self.s * 1.2), self.s * 3,
                                       self.s, color=(100, 0, 0),
                                       dark_color=(50, 0, 0))
        self.archer_button = Button('Лучник', round(self.s * 1.2), self.s * 3,
                                    round(self.s * 2.5), color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.cavalry_button = Button('Кавалерия', round(self.s * 1.2), self.s * 3,
                                     self.s * 4, color=(100, 0, 0),
                                     dark_color=(50, 0, 0))
        self.dragon_button = Button('Дракон', round(self.s * 1.2), self.s * 3,
                                    round(self.s * 5.5), color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.castle_button = Button('Замок', round(self.s * 1.2), self.s * 3,
                                    self.s * 7, color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.grass_button = Button('Трава', round(self.s * 1.2), self.s * 8,
                                   self.s, color=(100, 0, 0),
                                   dark_color=(50, 0, 0))
        self.rock_button = Button('Гора', round(self.s * 1.2), self.s * 8,
                                  round(self.s * 2.5), color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.hill_button = Button('Холм', round(self.s * 1.2), self.s * 8,
                                  self.s * 4, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.river_button = Button('Река', round(self.s * 1.2), self.s * 8,
                                   round(self.s * 5.5), color=(100, 0, 0),
                                   dark_color=(50, 0, 0))

        self.icons_units = pygame.sprite.Group()

        window.Window.set_lists(self, [self.back_button, self.swordsman_button, self.archer_button, self.cavalry_button,
                                       self.dragon_button, self.castle_button, self.grass_button, self.rock_button,
                                       self.hill_button, self.river_button])

        self.dct_units = {self.swordsman_button: swordsman.Swordsman,
                          self.archer_button: archer.Archer,
                          self.cavalry_button: cavalry.Cavalry,
                          self.dragon_button: dragon.Dragon,
                          self.castle_button: castle.Castle}

        self.dct_lands = {self.grass_button: ('grass', 'Трава', self.s * 16.1, self.s * 4.1,
                                              os.path.join('images', 'landscapes', 'grass.png'),
                                              self.s * 4, 0, 0, self.icons_units),
                          self.rock_button: ('mountains', 'Гора', self.s * 16.1, self.s * 4.1,
                                             os.path.join('images', 'landscapes', 'mountains.png'),
                                             self.s * 4, 0, 'нельзя', self.icons_units),
                          self.hill_button: ('../../hill', 'Холм', self.s * 16.1, self.s * 4.1,
                                             os.path.join('images', 'landscapes', 'hill.png'),
                                             self.s * 4, 15, -1, self.icons_units),
                          self.river_button: ('../../river', 'Река', self.s * 16.1, self.s * 4.1,
                                              os.path.join('images', 'landscapes', 'river.png'),
                                              self.s * 4, 0, 'Частично', self.icons_units)}

        self.stats = []

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))

    def check_click(self, mouse_pos, lst):
        self.icons_units.empty()
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.back_button:
                    self.running = False
                elif button in self.dct_units.keys():
                    self.icon_unit = self.dct_units[button](self.s * 16.1, self.s * 4.1,
                                                            self.s * 4, self.icons_units, None)
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

    @window.Window.render_decorator
    def render(self):
        if len(self.icons_units):
            pygame.draw.rect(self.screen, (66, 44, 33), (self.s * 10, self.s,
                                                         self.s * 11, self.s * 9), 8)
            pygame.draw.rect(self.screen, (0, 0, 0), (self.s * 16, self.s * 4,
                                                      self.s * 4.2, self.s * 4.2), 8)
            y = 50
            for i in reversed(self.stats):
                font = pygame.font.Font(None, round(self.s * 0.5))
                text = font.render(i, True, 'black')
                self.screen.blit(text, (self.s * 11, self.s * 8 - y))
                y += 50

            self.icons_units.draw(self.screen)

        f = pygame.font.Font(None, round(self.s * 1.3))
        t = f.render('Информация', True, 'black')
        self.main_screen.sc.blit(t, (self.s * 11, self.s * 2))

    @window.Window.start_decoration
    def start(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_LEFT:
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
