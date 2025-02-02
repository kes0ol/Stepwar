import sys

import pygame

import mapping

from global_vars import FILL_TYPE_BORDER
from widgets import Button, View


class Settings_window(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.volume = 0.4
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.volume_title = View('Громкость', self.one_size, self.width // 2, self.one_size, color=(255, 255, 0))
        self.plus_button = Button('+', self.one_size * 2, self.width // 2 + self.one_size * 3, self.one_size * 3,
                                  color=(0, 255, 0), dark_color=(0, 100, 0), fill_type=FILL_TYPE_BORDER)
        self.minus_button = Button('-', self.one_size * 2, self.width // 2 - self.one_size * 3, self.one_size * 3,
                                   color=(255, 0, 0), dark_color=(100, 0, 0), fill_type=FILL_TYPE_BORDER)
        self.percent_view = View(f'{int(self.volume * 100)}%', self.one_size, self.width // 2, self.one_size * 3,
                                 color=(255, 255, 0))
        self.reset_button = Button('Сбросить прогрес', self.one_size, self.one_size * 18, self.one_size * 11,
                                   color=(255, 255, 0), dark_color=(100, 100, 0))
        self.back_button = Button('Назад', self.one_size, self.one_size * 2, self.one_size * 11, color=(150, 0, 0),
                                  dark_color=(100, 0, 0))

        self.lst_buttons = [self.plus_button, self.minus_button, self.reset_button,
                            self.back_button]
        self.lst_views = [self.volume_title, self.percent_view]

        self.fon = pygame.image.load('images/backgrounds/settings_background.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                if button == self.plus_button and self.volume + 0.2 <= 1:
                    self.volume += 0.2
                    self.percent_view.set_text(f'{int(self.volume * 100)}%')

                    pygame.mixer.music.set_volume(self.volume)
                if button == self.minus_button and self.volume - 0.2 >= 0:
                    self.volume -= 0.2
                    self.percent_view.set_text(f'{int(self.volume * 100)}%')

                    pygame.mixer.music.set_volume(self.volume)

                if button == self.reset_button:
                    self.running = False
                    self.main_screen.reset_progress()
                    self.main.go_start_window()

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        for view in self.lst_views:
            view.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))
        self.main_screen.render_cursor()

    def start(self):
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
