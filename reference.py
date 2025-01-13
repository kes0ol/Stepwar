import sys

import pygame
import settings
import levels
from widgets import Button


class Reference_Window:
    def __init__(self, screen, size):
        self.running = True
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((self.width, self.height))


        self.back_button = Button('Назад в Главное меню', 80, self.width // 2, self.height // 2 + 200,
                                  color=(255, 255, 0), dark_color=(100, 0, 0))

        self.lst_buttons = [self.back_button]

        self.fon = pygame.image.load('images/fon.png')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

        self.text = 'лучник-дальник'

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False

    def render(self):

        self.main_screen.sc.blit(self.fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render(f'{self.text}', True, 'white')
        self.screen.blit(text, (self.width // 2, self.height // 2))
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
