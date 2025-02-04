import os.path

import pygame

from internal.different.widgets import Button, View
from internal.windows import window


class Final_window(window.Window):
    '''Создание класса финального экрана'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'final_background.png'))

        self.back_button = Button('Назад', round(self.s * 1.2), round(self.s * 1.7), self.height - self.s,
                                  color=(200, 75, 75), dark_color=(150, 25, 25))  # кнопка выхода

        self.win_view = View('Поздравляем!', self.s, self.width // 2, self.s * 2,
                             color=(255, 255, 0))  # сообщение поздравления

        window.Window.set_lists(self, [self.back_button, ], [self.win_view, ])

    def check_click(self, mouse_pos, lst):
        '''Функция проверка клика на кнопку выхода'''
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                    self.main_screen.reset_progress()
                    self.main.go_start_window()

    @window.Window.render_decorator
    def render(self):
        '''Отображение содержимого на экране'''
        self.render_info()

    def render_info(self):
        pass  # ОТОБРАЖЕНИЕ ФИНАЛЬНОЙ ИНФЫ В ФИНАЛЬНОМ ЭКРАНЕ

    @window.Window.start_decoration
    def start(self, event):
        '''Функция старта основного цикла программы'''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.main_screen.reset_progress()
                self.main.go_start_window()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
