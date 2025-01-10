import sys

import pygame
import settings
from widgets import Button


class Start_window:
    def __init__(self, screen, size):
        self.running = True
        self.size = self.width, self.height = size
        self.main_screen = screen

        self.choose_level = Button('Уровни', 80, self.width // 2, self.height // 2 - 400, color=(255, 255, 0),
                                   dark_color=(0, 255, 0))

        self.play_game_button = Button('Запустить игру', 80, self.width // 2, self.height // 2 - 200,
                                       color=(255, 255, 0),
                                       dark_color=(0, 255, 0))
        self.setting_button = Button('Настройки', 80, self.width // 2, self.height // 2, color=(255, 255, 0),
                                     dark_color=(50, 50, 50))
        self.exit_button = Button('Выйти', 80, self.width // 2, self.height // 2 + 200, color=(255, 255, 0),
                                  dark_color=(100, 0, 0))

        self.lst_buttons = [self.play_game_button, self.setting_button, self.exit_button, self.choose_level]

        self.settings_screen = settings.Settings_window(self.main_screen, self.size)

        self.fon = pygame.image.load('images/fon.png')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.play_game_button:
                    self.running = False
                if button == self.setting_button:
                    self.settings_screen.start()
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
        fps = 120
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
