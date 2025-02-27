import os

import pygame

from internal.basic.start_game import set_music
from internal.different.widgets import Button
from internal.windows import window


class Levels_menu(window.Window):
    '''Создание класса меню уровней'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'menu_levels_back_ground.jpg'))
        # создание кнопок
        self.first_level_button = Button('Уровень 1', 100, self.s * 4, self.height // 2,
                                         color=(40, 120, 80), dark_color=(40, 150, 80))
        self.second_level_button = Button('Уровень 2', 100, self.s * 11, self.height // 2,
                                          color=(40, 80, 120), dark_color=(40, 80, 150))
        self.thirst_level_button = Button('Уровень 3', 100, self.s * 18, self.height // 2,
                                          color=(120, 80, 40), dark_color=(150, 80, 40))
        self.back_button = Button('Назад', 80, self.width // 2, self.height // 2 + 200, color=(130, 130, 130))

        window.Window.set_lists(self, [self.back_button, ])  # список кнопок

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))  # звук клика

    def check_click(self, mouse_pos, lst):
        '''Проверка на клик по кнопкам мышкой'''
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.first_level_button and 1 in self.main_screen.progress:
                    self.running = False
                    set_music('music/first.wav', -1, 20)
                    self.main.start('1')
                if button == self.second_level_button and 2 in self.main_screen.progress:
                    self.running = False
                    set_music('music/second.wav', -1, 20)
                    self.main.start('2')
                if button == self.thirst_level_button and 3 in self.main_screen.progress:
                    self.running = False
                    set_music('music/final.wav', -1, 20)
                    self.main.start('3')
                if button == self.back_button:
                    self.running = False
                    self.main.go_start_window()

    @window.Window.render_decorator
    def render(self):
        '''Рендер уровней'''
        if 1 in self.main_screen.progress and self.first_level_button not in self.lst_buttons:
            self.lst_buttons.append(self.first_level_button)
        if 2 in self.main_screen.progress and self.second_level_button not in self.lst_buttons:
            self.lst_buttons.append(self.second_level_button)
        if 3 in self.main_screen.progress and self.thirst_level_button not in self.lst_buttons:
            self.lst_buttons.append(self.thirst_level_button)

    @window.Window.start_decoration
    def start(self, event):
        '''Функция начала основного цикла окна уровней'''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.main.go_start_window()
            if event.key == pygame.K_1 and 1 in self.main_screen.progress:
                self.running = False
                set_music('music/first.wav', -1, 20)
                self.main.start('1')
            if event.key == pygame.K_2 and 2 in self.main_screen.progress:
                self.running = False
                set_music('music/second.wav', -1, 20)
                self.main.start('2')
            if event.key == pygame.K_3 and 3 in self.main_screen.progress:
                self.running = False
                set_music('music/final.wav', -1, 20)
                self.main.start('3')
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
