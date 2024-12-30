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

        self.play_game_button = mapping.Button('Запустить игру', 80, 500, height // 2 - 300, 500, height // 2 - 300,
                                               True)
        self.setting_button = mapping.Button('    Настройки    ', 80, 500, height // 2 - 150, 500, height // 2 - 150,
                                             True, color=(100, 100, 100), dark_color=(50, 50, 50))
        self.exit_button = mapping.Button('        Выйти        ', 80, 500, height // 2, 500, height // 2, True,
                                          color=(150, 25, 25), dark_color=(100, 0, 0))

        self.lst_buttons = [self.play_game_button, self.setting_button, self.exit_button]

        self.settings_screen = settings.Settings_window(self.main_screen, self.size)

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
        for button in self.lst_buttons:
            self.screen.blit(button.button_surface, (button.button_rect.x, button.button_rect.y))
            self.screen.blit(button.text, button.button_rect)

            button.check_collidepoint(button.rect_width, button.rect_height)
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
