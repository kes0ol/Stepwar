import pygame

from development.different.widgets import Button
from development.windows import window


class Levels_menu(window.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main, ('images', 'backgrounds', 'menu_levels_back_ground.jpg'))

        self.first_level_button = Button('Уровень 1', 100, self.one_size * 4, self.height // 2,
                                         color=(40, 120, 80), dark_color=(40, 150, 80))
        self.second_level_button = Button('Уровень 2', 100, self.one_size * 11, self.height // 2,
                                          color=(40, 80, 120), dark_color=(40, 80, 150))
        self.thirst_level_button = Button('Уровень 3', 100, self.one_size * 18, self.height // 2,
                                          color=(120, 80, 40), dark_color=(150, 80, 40))
        self.back_button = Button('Назад', 80, self.width // 2, self.height // 2 + 200, color=(130, 130, 130))

        window.Window.set_lists(self, [self.back_button, ])

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.first_level_button and 1 in self.main_screen.progress:
                    self.running = False
                    self.main.start('1')
                if button == self.second_level_button and 2 in self.main_screen.progress:
                    self.running = False
                    self.main.start('2')
                if button == self.thirst_level_button and 3 in self.main_screen.progress:
                    self.running = False
                    self.main.start('3')
                if button == self.back_button:
                    self.running = False
                    self.main.go_start_window()

    @window.Window.render_decorator
    def render(self):
        if 1 in self.main_screen.progress and self.first_level_button not in self.lst_buttons:
            self.lst_buttons.append(self.first_level_button)
        if 2 in self.main_screen.progress and self.second_level_button not in self.lst_buttons:
            self.lst_buttons.append(self.second_level_button)
        if 3 in self.main_screen.progress and self.thirst_level_button not in self.lst_buttons:
            self.lst_buttons.append(self.thirst_level_button)

    @window.Window.start_decoration
    def start(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.main.go_start_window()
            if event.key == pygame.K_1 and 1 in self.main_screen.progress:
                self.running = False
                self.main.start('1')
            if event.key == pygame.K_2 and 2 in self.main_screen.progress:
                self.running = False
                self.main.start('2')
            if event.key == pygame.K_3 and 3 in self.main_screen.progress:
                self.running = False
                self.main.start('3')
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
