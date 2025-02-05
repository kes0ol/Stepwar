import os
from datetime import datetime

import pygame

import internal.different.global_vars as global_vars
from internal.db.score_report import ScoreReport
from internal.different.widgets import Button
from internal.windows import window


class Score_window(window.Window):  # класс окна счёта
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main, ('images', 'backgrounds', 'score.PNG'))
        self.screen = pygame.surface.Surface((self.width, self.height))
        # создание кнопок
        self.back_button = Button('Назад', self.s, self.s * 2, self.s * 11, color=(150, 0, 0),
                                  dark_color=(100, 0, 0))
        self.next_page_button = Button('>', self.s, self.s * 21, self.s * 11, color=(150, 0, 0),
                                       dark_color=(100, 0, 0))
        self.pref_page_button = Button('<', self.s, self.s * 20, self.s * 11, color=(150, 0, 0),
                                       dark_color=(100, 0, 0))
        self.page = 0
        # титулы страниц
        self.page_titles = ['Все результаты',
                            'Все результаты 1 уровень',
                            'Все результаты 2 уровень',
                            'Все результаты 3 уровень',
                            'Мои результаты',
                            'Мои результаты 1 уровень',
                            'Мои результаты 2 уровень',
                            'Мои результаты 3 уровень']

        window.Window.set_lists(self, [self.back_button, self.next_page_button, self.pref_page_button])  # список кнопок

        self.click_sound = pygame.mixer.Sound(os.path.join(*['music', 'click.wav']))  # звук клика

    def check_click(self, mouse_pos, lst):  # анализ клика
        for button in lst:
            if button.check_click(mouse_pos):
                self.click_sound.play()
                if button == self.back_button:
                    self.running = False
                if button == self.next_page_button:
                    self.page += 1
                    self.page %= len(self.page_titles)
                if button == self.pref_page_button:
                    self.page -= 1
                    self.page %= len(self.page_titles)

    @window.Window.render_decorator
    def render(self):  # отрисовка
        self.render_result_table()

    def render_result_table(self):  # отрисовка таблицы
        f = pygame.font.Font(None, 100)
        f_table = pygame.font.Font(None, int(self.s * 0.5))
        t = f.render(self.page_titles[self.page], True, 'red')
        self.screen.blit(t, (self.width // 2 - t.get_width() // 2, self.s * 1))

        limit = 10
        page_result_args = [
            {"limit": limit},
            {"level": 1, "limit": limit},
            {"level": 2, "limit": limit},
            {"level": 3, "limit": limit},
            {"user_id": global_vars.current_user.id, "limit": limit},
            {"user_id": global_vars.current_user.id, "level": 1, "limit": limit},
            {"user_id": global_vars.current_user.id, "level": 2, "limit": limit},
            {"user_id": global_vars.current_user.id, "level": 3, "limit": limit}
        ]
        results = ScoreReport.get(**page_result_args[self.page])

        x = [
            self.s,
            self.s * 12,
            self.s * 14,
            self.s * 15,
            self.s * 19
        ]
        title_y = self.s * 2
        y = self.s * 2.5
        dy = self.s * 0.5
        for j, v in enumerate(['Игрок', 'Уровень', 'Счет', 'Начало', 'Длительность']):
            self.screen.blit(f_table.render(str(v), True, 'red'), (x[j], title_y))
        for i, r in enumerate(results):
            for j, v in enumerate([r.user_nickname, r.level, r.score_points, r.created_at,
                                   datetime.fromisoformat(r.updated_at) - datetime.fromisoformat(r.created_at)]):
                self.screen.blit(f_table.render(str(v), True, 'red'), (x[j], y + i * dy))

    @window.Window.start_decoration
    def start(self, event):  # старт окна
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                if event.key == pygame.K_LEFT:
                    self.page += 1
                    self.page %= len(self.page_titles)
                if event.key == pygame.K_RIGHT:
                    self.page -= 1
                    self.page %= len(self.page_titles)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
