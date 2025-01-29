import sys

import pygame
import mapping
import settings
import levels
import reference
import shop
import score

from widgets import Button


class Start_window(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)

        y_pos = self.one_size * 1.8

        self.choose_level_button = Button('Уровни', round(self.one_size * 1.5), self.width // 2, y_pos,
                                          color=(255, 255, 0), dark_color=(0, 255, 0))
        self.shop_button = Button('Магазин', round(self.one_size * 1.5), self.width // 2, y_pos * 2,
                                  color=(255, 255, 0), dark_color=(0, 255, 0))
        self.setting_button = Button('Настройки', round(self.one_size * 1.5), self.width // 2, y_pos * 3,
                                     color=(255, 255, 0), dark_color=(50, 50, 50))
        self.ref_button = Button('Справка', round(self.one_size * 1.5), self.width // 2, y_pos * 4,
                                 color=(255, 255, 0), dark_color=(0, 255, 0))
        self.score_button = Button('Счёт', round(self.one_size * 1.5), self.width // 2, y_pos * 5,
                                   color=(255, 255, 0), dark_color=(0, 255, 0))
        self.exit_button = Button('Выйти', round(self.one_size * 1.5), self.width // 2, y_pos * 6,
                                  color=(255, 255, 0), dark_color=(100, 0, 0))

        self.lst_buttons = [self.setting_button, self.exit_button, self.choose_level_button,
                            self.ref_button, self.shop_button, self.score_button]

        self.settings_screen = settings.Settings_window(self.main_screen, self.size, main)
        self.ref_screen = reference.Reference_window(self.main_screen, self.size, main)
        self.levels_menu = levels.Levels_menu(self.main_screen, self.size, main)
        self.store = shop.Store(self.main_screen, self.size, main)
        self.score = score.Score_window(self.main_screen, self.size, main)

        self.fon = pygame.image.load('images/backgrounds/fon.PNG')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.choose_level_button:
                    self.levels_menu.start()
                if button == self.setting_button:
                    self.settings_screen.start()
                if button == self.ref_button:
                    self.ref_screen.start()
                if button == self.shop_button:
                    self.store.start()
                if button == self.score_button:
                    self.score.start()
                if button == self.exit_button:
                    self.running = False
                    pygame.quit()
                    sys.exit()

    def render(self):
        self.main_screen.sc.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.render_cursor()

    def start(self):
        fps = 60
        clock = pygame.time.Clock()

        dct_buttons = {pygame.K_1: self.levels_menu.start,
                       pygame.K_2: self.store.start,
                       pygame.K_3: self.settings_screen.start,
                       pygame.K_4: self.ref_screen.start}

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
                        pygame.quit()
                        sys.exit()
                    if event.key in dct_buttons.keys():
                        dct_buttons[event.key]()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
