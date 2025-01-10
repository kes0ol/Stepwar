import sys

import pygame
import settings
import levels
from widgets import Button


class Start_window:
    def __init__(self, screen, size):
        self.running = True
        self.size = width, height = size
        self.main_screen = screen
        self.screen = screen

        self.choose_level_button = Button('Уровни', 80, width // 2, height // 2 - 400, color=(255, 255, 0),
                                       dark_color=(0, 255, 0))

        self.play_game_button = Button('Запустить игру', 80, width // 2, height // 2 - 200, color=(255, 255, 0),
                                       dark_color=(0, 255, 0))
        self.setting_button = Button('Настройки', 80, width // 2, height // 2, color=(255, 255, 0),
                                     dark_color=(50, 50, 50))
        self.exit_button = Button('Выйти', 80, width // 2, height // 2 + 200, color=(255, 255, 0),
                                  dark_color=(100, 0, 0))

        self.lst_buttons = [self.play_game_button, self.setting_button, self.exit_button, self.choose_level_button]

        self.settings_screen = settings.Settings_window(self.main_screen, self.size)
        self.levels_menu = levels.Levels_menu(self.main_screen, self.size)

        self.fon = pygame.image.load('images/fon.png')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

        self.cursor = pygame.image.load('images/cursor.PNG')
        self.cursor.set_colorkey((255, 255, 255))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.choose_level_button:
                    self.levels_menu.start()
                if button == self.play_game_button:
                    self.running = False
                if button == self.setting_button:
                    self.settings_screen.start()
                if button == self.exit_button:
                    pygame.quit()
                    sys.exit()

    def render(self):
        self.screen.sc.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen.sc)

    def start(self):
        fps = 120
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.main_screen.sc.blit(self.cursor, (event.pos[0], event.pos[1]))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
