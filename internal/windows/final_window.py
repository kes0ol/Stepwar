import os

import pygame

from internal.basic.start_game import set_music
from internal.different.global_vars import UNIT_SWORDSMAN, UNIT_ARCHER, UNIT_CAVALRY, UNIT_DRAGON
from internal.different.widgets import Button, View
from internal.windows import window


class Final_window(window.Window):
    '''Создание класса финального экрана'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'final_background.jpg'))

        self.back_button = Button('Назад', round(self.s * 1.2), round(self.s * 1.7), self.height - self.s,
                                  color=(200, 75, 75), dark_color=(150, 25, 25))  # кнопка выхода

        self.win_view = View('Поздравляем!', self.s, self.width // 2, self.s * 2,
                             color=(255, 255, 0))  # сообщение поздравления

        window.Window.set_lists(self, [self.back_button, ], [self.win_view, ])

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))

    def render_info(self):
        info = (('Общий счёт:', self.main.screen.summary_score),
                ('Лучший счёт:', self.main.screen.best_score),
                ('', ''),
                ('Всего убито юнитов:', sum(self.main.screen.en_un_dead.values())),
                ('Убито рыцарей:', self.main.screen.en_un_dead[UNIT_SWORDSMAN]),
                ('Убито лучников', self.main.screen.en_un_dead[UNIT_ARCHER]),
                ('Убито кавалерии:', self.main.screen.en_un_dead[UNIT_CAVALRY]),
                ('Убито драконов:', self.main.screen.en_un_dead[UNIT_DRAGON]),
                ('', ''),
                ('Всего потеряно юнитов:', sum(self.main.screen.my_un_dead.values())),
                ('Потеряно рыцарей:', self.main.screen.my_un_dead[UNIT_SWORDSMAN]),
                ('Потеряно лучников:', self.main.screen.my_un_dead[UNIT_ARCHER]),
                ('Потеряно кавалерии:', self.main.screen.my_un_dead[UNIT_CAVALRY]),
                ('Потеряно драконов:', self.main.screen.my_un_dead[UNIT_DRAGON]))

        y = self.s * 3
        f = pygame.font.Font(None, self.s // 2)
        for i in info:
            t = f.render('   '.join(list(map(str, i))), True, 'white')
            self.screen.blit(t, (self.s * 2, y))
            y += round(self.s / 2)

    def check_click(self, mouse_pos, lst):
        '''Функция проверка клика на кнопку выхода'''
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.back_button:
                    self.running = False
                    self.main_screen.reset_progress()
                    self.main.go_start_window()

    @window.Window.render_decorator
    def render(self):
        '''Отображение содержимого на экране'''
        self.render_info()

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
