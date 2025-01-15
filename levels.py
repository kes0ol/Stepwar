import sys

import pygame

from widgets import Button


class Levels_menu:
    def __init__(self, screen, size, main):
        self.size = width, height = size
        self.main_screen = screen
        self.main = main
        self.screen = pygame.surface.Surface((width, height))

        self.first_level_button = Button('Уровень 1', 100, width // 2 - 700, height // 2,
                                         color=(40, 120, 80), dark_color=(40, 150, 80))
        self.second_level_button = Button('Уровень 2', 100, width // 2, height // 2,
                                          color=(40, 80, 120), dark_color=(40, 80, 150))
        self.thirst_level_button = Button('Уровень 3', 100, width // 2 + 600, height // 2,
                                          color=(120, 80, 40), dark_color=(150, 80, 40))
        self.back_button = Button('Назад', 80, width // 2, height // 2 + 200, color=(130, 130, 130))

        self.lst_buttons = [self.first_level_button, self.second_level_button, self.thirst_level_button,
                            self.back_button]

        self.fon = pygame.image.load('images/menu_levels_fon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.first_level_button:
                    self.running = False
                    self.main.start('1')
                if button == self.second_level_button:
                    self.running = False
                    self.main.start('2')
                if button == self.thirst_level_button:
                    self.running = False
                    self.main.start('3')
                if button == self.back_button:
                    self.running = False
                    self.main.go_start_window()

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))
        self.main_screen.render_cursor()

    def start(self):
        fps = 120
        clock = pygame.time.Clock()

        self.running = True
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
