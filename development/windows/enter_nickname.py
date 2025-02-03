import os
import sys

import pygame

import development.basic.mapping as mapping

import development.different.global_vars as global_vars
from development.db.user_dbo import User
from development.different.widgets import Button, Edit, View


class EnterNicknameWindow(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.view = View('Введите Ваше имя:', self.one_size, self.width // 2, self.height // 2 - self.one_size,
                                  color=(150, 150, 0))
        self.next_button = Button('Подтвердить', self.one_size, self.width // 2, self.height // 2 + self.one_size,
                                  color=(150, 150, 0), dark_color=(100, 0, 0))
        self.exit_button = Button('Выйти', self.one_size, self.width // 2, self.height // 2 + self.one_size * 4,
                                  color=(150, 150, 0), dark_color=(100, 0, 0))
        self.edit = Edit('Username', self.one_size, self.width // 2, self.height // 2,
                         self.width - self.one_size * 8, self.one_size)
        self.ui = [self.view, self.next_button, self.exit_button, self.edit]
        self.fon = pygame.image.load(os.path.join('images', 'backgrounds', 'settings_background.jpg'))
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

        self.running = False

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

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for ui in self.ui:
            ui.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))
        self.main_screen.render_cursor()

    def start(self):
        if global_vars.current_user:
            return
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
