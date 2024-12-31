import sys

import pygame
import mapping
import start_window


class Settings_window:
    def __init__(self, screen, size):
        self.volume = 1
        self.running = True
        self.size = width, height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((width, height))

        self.plus_button = mapping.Button('  +  ', 150, 800, height // 2 - 160, 1100, height // 2 - 160, 1100,
                                          color=(0, 255, 0), dark_color=(0, 100, 0))
        self.minus_button = mapping.Button('  -  ', 150, 800, height // 2 - 160, 790, height // 2 - 160, 790,
                                           color=(255, 0, 0), dark_color=(100, 0, 0))
        self.volume_button = mapping.Button('  Громкость  ', 80, 850, height // 2 - 320, 850, height // 2 - 320, False,
                                            color=(255, 255, 0), dark_color=(255, 255, 0))
        self.back_button = mapping.Button('      Назад      ', 80, 850, height // 2, 850, height // 2, True,
                                          color=(255, 255, 0), dark_color=(100, 100, 0))

        self.lst_buttons = [self.volume_button, self.plus_button, self.minus_button, self.back_button]
        self.fon = pygame.image.load('images/settingsfon.jpg')
        self.fon = pygame.transform.scale(self.fon, (size[0], size[1]))

    def check_click(self, mouse_pos, lst):
        p = False
        for button in lst:
            if (button.button_rect.left <= mouse_pos[0] <= button.button_rect.right and
                    button.button_rect.top <= mouse_pos[1] <= button.button_rect.bottom):
                if button == self.back_button:
                    self.running = False
                if button == self.plus_button and self.volume < 1:
                    self.volume += 0.2
                    # pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(self.volume)
                if button == self.minus_button and self.volume > 0:
                    self.volume -= 0.2
                    # pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(self.volume)


    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        self.main_screen.blit(self.screen, (0, 0))

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
