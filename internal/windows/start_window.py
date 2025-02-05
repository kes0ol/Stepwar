import os
import sys

import pygame

from internal.different.widgets import Button
from internal.windows import levels, reference, score, settings, shop
from internal.windows import window


class Start_window(window.Window):
    '''Создание класса начального экрана'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'fon.PNG'))

        self.y_pos = self.s * 1.8

        # создание кнопок
        self.choose_level_button = Button('Уровни', round(self.s * 1.5), self.width // 2, self.y_pos,
                                          color=(255, 255, 0), dark_color=(0, 255, 0))  # кнопка уровней
        self.shop_button = Button('Магазин', round(self.s * 1.5), self.width // 2, self.y_pos * 2,
                                  color=(255, 255, 0), dark_color=(0, 255, 0))  # кнопка магазина
        self.setting_button = Button('Настройки', round(self.s * 1.5), self.width // 2, self.y_pos * 3,
                                     color=(255, 255, 0), dark_color=(50, 50, 50))  # кнопка настроек
        self.ref_button = Button('Справка', round(self.s * 1.5), self.width // 2, self.y_pos * 4,
                                 color=(255, 255, 0), dark_color=(0, 255, 0))  # кнопка справок
        self.score_button = Button('Счёт', round(self.s * 1.5), self.width // 2, self.y_pos * 5,
                                   color=(255, 255, 0), dark_color=(0, 255, 0))  # кнопка счёта
        self.exit_button = Button('Выйти', round(self.s * 1.5), self.width // 2, self.y_pos * 6,
                                  color=(255, 255, 0), dark_color=(100, 0, 0))  # кнопка выхода

        window.Window.set_lists(self, [self.setting_button, self.exit_button, self.choose_level_button,
                                       self.ref_button, self.shop_button, self.score_button])

        self.settings_screen = settings.Settings_window(self.main_screen, self.size, main)  # экран настроек
        self.ref_screen = reference.Reference_window(self.main_screen, self.size, main)  # экран справки
        self.levels_menu = levels.Levels_menu(self.main_screen, self.size, main)  # экран уровней
        self.store = shop.Store(self.main_screen, self.size, main)  # экран магазина
        self.score = score.Score_window(self.main_screen, self.size, main)  # экран очков

        self.dct_buttons = {pygame.K_1: self.levels_menu.start,
                            pygame.K_2: self.store.start,
                            pygame.K_3: self.settings_screen.start,
                            pygame.K_4: self.ref_screen.start}

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))# звук клика

    def check_click(self, mouse_pos, lst):
        '''Проверка на клик по кнопкам мышкой'''
        dct = {self.choose_level_button: self.levels_menu.start,
               self.setting_button: self.settings_screen.start,
               self.ref_button: self.ref_screen.start,
               self.shop_button: self.store.start,
               self.score_button: self.score.start,
               }
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.exit_button:  # если кнопка выхода
                    self.running = False
                    pygame.quit()
                    sys.exit()
                else:  # в зависимости от кнопки вызов функции
                    dct[button]()

    @window.Window.render_decorator
    def render(self):
        '''Рендер стартового экрана'''
        pass

    @window.Window.start_decoration
    def start(self, event):
        '''Функция старта основного цикла стартового окна'''
        if event.type == pygame.KEYDOWN:  # проверка нажатия клавиш
            if event.key == pygame.K_ESCAPE:  # если нажат escape
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_e:
                self.main.go_final_window()
            if event.key in self.dct_buttons.keys():  # в зависимости от кнопки
                self.dct_buttons[event.key]()
        if event.type == pygame.MOUSEBUTTONDOWN:  # при нажатии мышкой
            self.check_click(event.pos, self.lst_buttons)
