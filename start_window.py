import sys

import pygame
import mapping
import settings


class Start_window:
    def __init__(self, screen, size):
        self.running = True
        self.size = width, height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((width, height))

        self.play_game_button = mapping.Button('Запустить игру', 80, 800, height // 2 - 200, 800, height // 2 - 170,
                                               True, color=(255, 255, 0), dark_color=(0, 255, 0))
        self.setting_button = mapping.Button('    Настройки    ', 80, 800, height // 2 - 40 , 800, height // 2 - 40,
                                             True, color=(255, 255, 0), dark_color=(50, 50, 50))
        self.exit_button = mapping.Button('        Выйти        ', 80, 800, height // 2 + 100, 800, height // 2 + 100,
                                          True,
                                          color=(255, 255, 0), dark_color=(100, 0, 0))

        self.lst_buttons = [self.play_game_button, self.setting_button, self.exit_button]

        self.settings_screen = settings.Settings_window(self.main_screen, self.size)
        self.fon = pygame.image.load('images/fon.PNG')
        self.fon = pygame.transform.scale(self.fon, (size[0], size[1]))

        self.cursor = pygame.image.load('images/cursor.PNG')
        self.cursor.set_colorkey((255, 255, 255))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if (button.button_rect.left <= mouse_pos[0] <= button.button_rect.right and
                    button.button_rect.top <= mouse_pos[1] <= button.button_rect.bottom):
                if button == self.play_game_button:
                    self.running = False
                if button == self.setting_button:
                    self.settings_screen.start()
                if button == self.exit_button:
                    pygame.quit()
                    sys.exit()

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        self.main_screen.blit(self.screen, (0, 0))

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
                    self.main_screen.blit(self.cursor, (event.pos[0], event.pos[1]))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
