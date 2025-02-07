import os

import pygame

from internal.different.global_vars import FILL_TYPE_BORDER
from internal.different.widgets import Button, View
from internal.windows import window


class Settings_window(window.Window):
    '''Создание класса настроек'''
    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'settings_background.jpg'))
        self.volume = 1  # начальная громкость
        # создание кнопок
        self.volume_title = View('Громкость', self.s, self.width // 2, self.s, color=(255, 255, 0))
        self.percent_view = View(f'{self.volume * 100}%', self.s, self.width // 2, self.s * 3,
                                 color=(255, 255, 0))
        self.plus_button = Button('+', self.s * 2, self.width // 2 + self.s * 3, self.s * 3,
                                  color=(0, 255, 0), dark_color=(0, 100, 0), fill_type=FILL_TYPE_BORDER)
        self.minus_button = Button('-', self.s * 2, self.width // 2 - self.s * 3, self.s * 3,
                                   color=(255, 0, 0), dark_color=(100, 0, 0), fill_type=FILL_TYPE_BORDER)
        self.reset_button = Button('Сбросить прогрес', self.s, self.s * 18, self.s * 11,
                                   color=(255, 255, 0), dark_color=(100, 100, 0))
        self.back_button = Button('Назад', self.s, self.s * 2, self.s * 11, color=(150, 0, 0),
                                  dark_color=(100, 0, 0))

        window.Window.set_lists(self, [self.plus_button, self.minus_button, self.reset_button,
                                       self.back_button], [self.volume_title, self.percent_view])  # список кнопок

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))  # звук клика

    def check_click(self, mouse_pos, lst):
        '''Проверка на клик по кнопкам мышкой'''
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.back_button:
                    self.running = False
                if button == self.plus_button and self.volume + 0.2 <= 1:
                    self.volume += 0.2
                    self.percent_view.set_text(f'{int(self.volume * 100)}%')

                    pygame.mixer.music.set_volume(self.volume)
                if button == self.minus_button and self.volume - 0.2 >= 0:
                    self.volume -= 0.2
                    self.percent_view.set_text(f'{int(self.volume * 100)}%')

                    pygame.mixer.music.set_volume(self.volume)

                if button == self.reset_button:
                    self.running = False
                    self.main_screen.reset_progress()
                    self.main.go_start_window()

    @window.Window.render_decorator
    def render(self):
        '''Рендер настроек'''
        pass

    @window.Window.start_decoration
    def start(self, event):
        '''Функция проверок на нажатие'''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            if event.key in [pygame.K_MINUS, pygame.K_EQUALS]:
                if event.key == pygame.K_MINUS and self.volume - 0.2 >= 0:
                    self.volume -= 0.2
                if event.key == pygame.K_EQUALS and self.volume + 0.2 <= 1:
                    self.volume += 0.2
                self.percent_view.set_text(f'{int(self.volume * 100)}%')
                pygame.mixer.music.set_volume(self.volume)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
