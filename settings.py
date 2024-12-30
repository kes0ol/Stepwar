import sys

import pygame
import mapping


class Settings_window:
    def __init__(self, screen, size):
        self.running = True
        self.size = width, height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((width, height))

        self.volume_button = mapping.Button('  Громкость  ', 80, 500, height // 2 - 320, 500, height // 2 - 320, False,
                                            color=(0, 150, 0), dark_color=(0, 150, 0))
        self.off_volume_button = mapping.Button('  Turn off  ', 50, 200, height // 2 - 200, 200, height // 2 - 200,
                                                False, color=(100, 100, 100), dark_color=(100, 100, 100))
        self.twenty_volume_button = mapping.Button('  20%  ', 50, 400, height // 2 - 200, 400, height // 2 - 200, True,
                                                   color=(25, 25, 255), dark_color=(25, 25, 200))
        self.fourty_volume_button = mapping.Button('  40%  ', 50, 550, height // 2 - 200, 550, height // 2 - 200, True,
                                                   color=(50, 200, 220), dark_color=(25, 150, 200))
        self.sixty_volume_button = mapping.Button('  60%  ', 50, 700, height // 2 - 200, 700, height // 2 - 200, True,
                                                  color=(50, 220, 50), dark_color=(25, 150, 25))
        self.eighty_volume_button = mapping.Button('  80%  ', 50, 850, height // 2 - 200, 850, height // 2 - 200, True,
                                                   color=(240, 220, 25), dark_color=(200, 175, 0))
        self.hundred_volume_button = mapping.Button('  100%  ', 50, 1000, height // 2 - 200, 1000, height // 2 - 200,
                                                    True, color=(250, 150, 25), dark_color=(200, 125, 25))
        self.back_button = mapping.Button('      Назад      ', 80, 500, height // 2, 500, height // 2, True,
                                          color=(150, 25, 25), dark_color=(100, 0, 0))

        self.lst_buttons = [self.volume_button, self.off_volume_button, self.twenty_volume_button,
                            self.fourty_volume_button, self.sixty_volume_button, self.eighty_volume_button,
                            self.hundred_volume_button, self.back_button]

    def check_click(self, mouse_pos, lst):
        p = False
        for button in lst:
            if (button.button_rect.left <= mouse_pos[0] <= button.button_rect.right and
                    button.button_rect.top <= mouse_pos[1] <= button.button_rect.bottom):
                if button == self.back_button:
                    self.running = False
                elif button == self.off_volume_button:
                    pygame.mixer.music.pause()
                    # p = True
                elif button == self.twenty_volume_button:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.2)
                elif button == self.fourty_volume_button:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.4)
                elif button == self.sixty_volume_button:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.6)
                elif button == self.eighty_volume_button:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.8)
                elif button == self.hundred_volume_button:
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(1)

    def render(self):
        for button in self.lst_buttons:
            self.screen.blit(button.button_surface, (button.button_rect.x, button.button_rect.y))
            self.screen.blit(button.text, button.button_rect)

            button.check_collidepoint(button.rect_width, button.rect_height)
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
