import os
import sys

import pygame

from internal.db.user_dbo import User
from internal.different import global_vars
from internal.different.widgets import Button, Edit, View
from internal.windows import window


class EnterNicknameWindow(window.Window):
    '''Создание класса для ввода имени'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'settings_background.jpg'))
        self.screen = pygame.surface.Surface((self.width, self.height))
        # создание кнопок
        self.view = View('Введите Ваше имя:', self.s, self.width // 2, self.height // 2 - self.s,
                         color=(150, 150, 0))
        self.next_button = Button('Подтвердить', self.s, self.width // 2, self.height // 2 + self.s,
                                  color=(150, 150, 0), dark_color=(100, 0, 0))
        self.exit_button = Button('Выйти', self.s, self.width // 2, self.height // 2 + self.s * 4,
                                  color=(150, 150, 0), dark_color=(100, 0, 0))
        self.edit = Edit('Username', self.s, self.width // 2, self.height // 2,
                         self.width - self.s * 8, self.s)

        window.Window.set_lists(self, [self.next_button, self.exit_button], [self.view, self.edit])

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))  # звук клика

    def check_click(self, mouse_pos):
        '''Проверка на клик по кнопкам мышкой'''
        if self.next_button.check_click(mouse_pos):
            self.click_sound.play()
            if len(self.edit.text):

                user = User.get_by_nickname(self.edit.text)
                if user:
                    global_vars.current_user = user
                else:
                    global_vars.current_user = User(nickname=self.edit.text)
                    User.add(global_vars.current_user)

                self.running = False
        if self.exit_button.check_click(mouse_pos):
            self.running = False
            pygame.quit()
            sys.exit()
        if self.edit.check_click(mouse_pos):
            self.edit.start(self)

    @window.Window.render_decorator
    def render(self):
        '''Рендер окна для ввода имени'''
        if self.edit.edit_started:
            self.next_button.set_enabled(False)
        else:
            self.next_button.set_enabled(True)

    @window.Window.start_decoration
    def start(self, event):
        '''Функция начала основного цикла окна для ввода имени'''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos)
