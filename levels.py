import sys

import pygame

import mapping

from widgets import Button


class Levels_menu(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.first_level_button = Button('Уровень 1', 100, self.one_size * 4, self.height // 2,
                                         color=(40, 120, 80), dark_color=(40, 150, 80))
        self.second_level_button = Button('Уровень 2', 100, self.one_size * 11, self.height // 2,
                                          color=(40, 80, 120), dark_color=(40, 80, 150))
        self.thirst_level_button = Button('Уровень 3', 100, self.one_size * 18, self.height // 2,
                                          color=(120, 80, 40), dark_color=(150, 80, 40))
        self.back_button = Button('Назад', 80, self.width // 2, self.height // 2 + 200, color=(130, 130, 130))

        self.lst_buttons = [self.first_level_button, self.second_level_button, self.thirst_level_button,
                            self.back_button]

        self.fon = pygame.image.load('images/backgrounds/menu_levels_fon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.first_level_button and 1 in self.main_screen.progress:
                    self.main_screen.choose_level = 1
                    self.running = False
                    self.main.start('1')
                if button == self.second_level_button and 2 in self.main_screen.progress:
                    self.main_screen.choose_level = 2
                    self.running = False
                    self.main.start('2')
                if button == self.thirst_level_button and 3 in self.main_screen.progress:
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.main.go_start_window()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
