import sys

import pygame

from global_vars import FILL_TYPE_BORDER
from widgets import Button, View


class Settings_window:
    def __init__(self, screen, size):
        self.volume = 1
        self.running = True
        self.size = width, height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((width, height))

        self.volume_button = Button('Громкость', 80, width // 2, height // 2 - 400,
                                    color=(255, 255, 0), dark_color=(255, 255, 0))
        self.plus_button = Button('+', 150, width // 2 + 200, height // 2 - 200, color=(0, 255, 0),
                                  dark_color=(0, 100, 0), fill_type=FILL_TYPE_BORDER)
        self.minus_button = Button('-', 150, width // 2 - 200, height // 2 - 200,
                                   color=(255, 0, 0), dark_color=(100, 0, 0), fill_type=FILL_TYPE_BORDER)
        self.procent_view = View(f'{self.volume * 100}%', 80, width // 2, height / 2 - 200, color=(255, 255, 0))
        self.back_button = Button('Назад', 80, width // 2, height // 2, color=(255, 255, 0),
                                  dark_color=(100, 100, 0))

        self.lst_buttons = [self.volume_button, self.plus_button, self.minus_button, self.back_button]
        self.fon = pygame.image.load('images/settingsfon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                if button == self.plus_button and self.volume + 0.2 <= 1:
                    self.volume += 0.2
                    self.procent_view.set_text(f'{int(self.volume * 100)}%')

                    pygame.mixer.music.set_volume(self.volume)
                if button == self.minus_button and self.volume - 0.2 >= 0:
                    self.volume -= 0.2
                    self.procent_view.set_text(f'{int(self.volume * 100)}%')

                    pygame.mixer.music.set_volume(self.volume)

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        self.procent_view.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))

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
