import sys

import pygame

from development.db.user_dbo import User
from development.different import global_vars
from development.different.widgets import Button, Edit, View
from development.windows import window


class EnterNicknameWindow(window.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main, ('images', 'backgrounds', 'settings_background.jpg'))
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.view = View('Введите Ваше имя:', self.one_size, self.width // 2, self.height // 2 - self.one_size,
                         color=(150, 150, 0))
        self.next_button = Button('Подтвердить', self.one_size, self.width // 2, self.height // 2 + self.one_size,
                                  color=(150, 150, 0), dark_color=(100, 0, 0))
        self.exit_button = Button('Выйти', self.one_size, self.width // 2, self.height // 2 + self.one_size * 4,
                                  color=(150, 150, 0), dark_color=(100, 0, 0))
        self.edit = Edit('Username', self.one_size, self.width // 2, self.height // 2,
                         self.width - self.one_size * 8, self.one_size)

        window.Window.set_lists(self, [self.next_button, self.exit_button], [self.view, self.edit])

    def check_click(self, mouse_pos):
        if self.next_button.check_click(mouse_pos):
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
        pass

    @window.Window.start_decoration
    def start(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos)
