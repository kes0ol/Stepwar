import sys

import pygame

from widgets import Button


class Creators:
    def __init__(self, screen, size):
        self.volume = 1
        self.size = self.width, self.height = size
        self.main_screen = screen

        self.back_button = Button('Назад', 80, self.width // 2, self.height / 1.5, color=(100, 200, 0),
                                  dark_color=(100, 100, 0))
        self.lst_buttons = [self.back_button]

        self.lst = ['Ссылка на git страницу проекта : https://github.com/kes0ol/Stepwar',
                    '                         Авторы: Lvumbets&Kes0ol']

        self.fon = pygame.image.load('images/backgrounds/cfon.PNG')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False

    def render(self):
        y = 50
        self.main_screen.sc.blit(self.fon, (0, 0))
        for i in self.lst:
            font = pygame.font.Font(None, 40)
            text = font.render(i, True, 'black')
            self.main_screen.sc.blit(text, (self.width / 3.5, self.height // 2 - y))
            y += 50
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.sc.blit(self.main_screen.sc, (0, 0))
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
