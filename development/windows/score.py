from datetime import datetime

import pygame

import development.different.global_vars as global_vars
from development.db.score_dbo import Score
from development.different.widgets import Button
from development.windows import window


class Score_window(window.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main, ('images', 'backgrounds', 'score.PNG'))
        self.volume = 1
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.back_button = Button('Назад', self.one_size, self.one_size * 2, self.one_size * 11, color=(150, 0, 0),
                                  dark_color=(100, 0, 0))
        self.next_page_button = Button('>', self.one_size, self.one_size * 21, self.one_size * 11, color=(150, 0, 0),
                                       dark_color=(100, 0, 0))
        self.pref_page_button = Button('<', self.one_size, self.one_size * 20, self.one_size * 11, color=(150, 0, 0),
                                       dark_color=(100, 0, 0))
        self.page = 0

        self.page_titles = ['Все результаты',
                            'Все результаты 1 уровень',
                            'Все результаты 2 уровень',
                            'Все результаты 3 уровень',
                            'Мои результаты',
                            'Мои результаты 1 уровень',
                            'Мои результаты 2 уровень',
                            'Мои результаты 3 уровень']

        window.Window.set_lists(self, [self.back_button, ])

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                if button == self.next_page_button:
                    self.page += 1
                    self.page %= len(self.page_titles)
                if button == self.pref_page_button:
                    self.page -= 1
                    self.page %= len(self.page_titles)

    @window.Window.render_decorator
    def render(self):
        self.render_result_table()

    def render_result_table(self):
        f = pygame.font.Font(None, 100)
        f_table = pygame.font.Font(None, int(self.one_size * 0.5))
        t = f.render(self.page_titles[self.page], True, 'red')
        self.main_screen.sc.blit(t, (self.width // 2 - t.get_width() // 2, self.one_size * 1))

        limit = 10
        page_functions = [
            Score.get_ordered_by_score(limit),
            Score.get_by_level_ordered_by_score(1, limit),
            Score.get_by_level_ordered_by_score(2, limit),
            Score.get_by_level_ordered_by_score(3, limit),
            Score.get_by_user_ordered_by_score(global_vars.current_user.id, limit),
            Score.get_by_user_level_ordered_by_score(global_vars.current_user.id, 1, limit),
            Score.get_by_user_level_ordered_by_score(global_vars.current_user.id, 2, limit),
            Score.get_by_user_level_ordered_by_score(global_vars.current_user.id, 3, limit),
        ]
        results = page_functions[self.page]

        x = [
            self.one_size,
            self.one_size * 12,
            self.one_size * 14,
            self.one_size * 15,
            self.one_size * 19
        ]
        title_y = self.one_size * 2
        y = self.one_size * 2.5
        dy = self.one_size * 0.5
        for j, v in enumerate(['Игрок', 'Уровень', 'Счет', 'Начало', 'Длительность']):
            self.main_screen.sc.blit(f_table.render(str(v), True, 'red'), (x[j], title_y))
        for i, r in enumerate(results):
            for j, v in enumerate([r.user_nickname, r.level, r.score_points, r.created_at,
                                   datetime.fromisoformat(r.updated_at) - datetime.fromisoformat(r.created_at)]):
                self.main_screen.sc.blit(f_table.render(str(v), True, 'red'), (x[j], y + i * dy))

    @window.Window.start_decoration
    def start(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_click(event.pos, self.lst_buttons)
