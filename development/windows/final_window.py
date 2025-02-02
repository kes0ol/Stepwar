import pygame

import sys

from development.windows import window

from development.different.widgets import Button, View


class Final_window(window.Window):
    '''Создание класса финального экрана'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, '../../images/backgrounds/final_background.png')

        self.back_button = Button('Назад', round(self.one_size * 1.2), round(self.one_size * 1.7), self.height - 100,
                                  color=(200, 75, 75), dark_color=(150, 25, 25))  # кнопка выхода

        self.win_view = View('Поздравляем!', self.one_size, self.width // 2, self.one_size * 5,
                             color=(255, 255, 0))  # сообщение поздравления

        window.Window.set_lists(self, [self.back_button,], [self.win_view,])

    def check_click(self, mouse_pos):
        '''Функция проверка клика на кнопку выхода'''
        if self.back_button.check_click(mouse_pos):
            self.running = False
            self.main_screen.reset_progress()
            self.main.go_start_window()

    def render(self):
        '''Отображение содержимого на экране'''
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        for view in self.lst_views:
            view.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))
        self.main_screen.render_cursor()

    def start(self):
        '''Функция старта основного цикла программы'''
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:  # запуск основного цикла
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.main_screen.reset_progress()
                        self.main.go_start_window()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
