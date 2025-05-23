import os

import pygame

from internal.different.widgets import Button
from internal.windows import window


class About_Creators(window.Window):
    '''Создание класса об авторах'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'about_creators.jpg'))
        # создание кнопки

        self.back_button = Button('Назад', 80, self.width // 2, self.height // 2 + 200, color=(130, 130, 130))

        window.Window.set_lists(self, [self.back_button, ])  # список кнопок

        self.txt = ['git: "https://github.com/kes0ol/Stepwar"', 'Создатели: Кобышев Лев']

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))  # звук клика

    def check_click(self, mouse_pos, lst):
        '''Проверка на клик по кнопкам мышкой'''
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.back_button:
                    self.running = False
                    self.main.go_start_window()

    @window.Window.render_decorator
    def render(self):
        '''Рендер окна об авторах'''
        y = 100
        for i in self.txt:
            font = pygame.font.Font(None, round(self.s * 0.5))
            text = font.render(i, True, 'black')
            self.screen.blit(text, (self.s * 7 + y, self.s * 8 - y))
            y += 50

    @window.Window.start_decoration
    def start(self, event):  # старт окна
        '''Функция начала основного цикла окна об авторах'''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.main.go_start_window()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
