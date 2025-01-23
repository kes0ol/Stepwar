import sys

import pygame
import settings
import levels
import reference
import shop

from widgets import Button


class Start_window:
    def __init__(self, screen, size, main):
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.choose_level_button = Button('Уровни', 100, self.width // 2, self.height // 2 - 350, color=(255, 255, 0),
                                          dark_color=(0, 255, 0))
        self.shop_button = Button('Магазин', 100, self.width // 2, self.height // 2 - 200, color=(255, 255, 0),
                                  dark_color=(0, 255, 0))
        self.setting_button = Button('Настройки', 100, self.width // 2, self.height // 2 - 50, color=(255, 255, 0),
                                     dark_color=(50, 50, 50))
        self.ref_button = Button('Справка', 100, self.width // 2, self.height // 2 + 100, color=(255, 255, 0),
                                 dark_color=(0, 255, 0))
        self.exit_button = Button('Выйти', 100, self.width // 2, self.height // 2 + 250, color=(255, 255, 0),
                                  dark_color=(100, 0, 0))

        self.lst_buttons = [self.setting_button, self.exit_button, self.choose_level_button,
                            self.ref_button, self.shop_button]

        self.settings_screen = settings.Settings_window(self.main_screen, self.size)
        self.ref_screen = reference.Reference_window(self.main_screen, self.size, main)
        self.levels_menu = levels.Levels_menu(self.main_screen, self.size, main)
        self.store = shop.Store(screen, self.size)

        self.fon = pygame.image.load('images/backgrounds/fon.PNG')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))


        self.click_sound = pygame.mixer.Sound('music/click.wav')

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.choose_level_button:
                    self.click_sound.play()
                    self.running = False
                    self.levels_menu.start()
                if button == self.setting_button:
                    self.click_sound.play()
                    self.settings_screen.start()
                if button == self.ref_button:
                    self.click_sound.play()
                    self.ref_screen.start()
                if button == self.shop_button:
                    self.click_sound.play()
                    self.store.start()
                if button == self.exit_button:
                    self.click_sound.play()
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
