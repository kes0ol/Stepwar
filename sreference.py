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

        self.swordsman_button = Button('Мечник', 100, self.width // 4, self.height // 3, color=(100, 0, 0),
                                       dark_color=(50, 0, 0))

        self.back_button = Button('<-', 200, 80, self.height - 80,
                                  color=(100, 0, 0), dark_color=(50, 0, 0))

        self.lst_buttons = [self.back_button, self.swordsman_button]

        # self.lst = ['gggg']

        self.fon = pygame.image.load('images/reffon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))


    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False

    def render(self):
        # y = 50
        self.main_screen.sc.blit(self.fon, (0, 0))
        # for i in self.lst:
        #     font = pygame.font.Font(None, 40)
        #     text = font.render(i, True, 'black')
        #     self.main_screen.sc.blit(text, (self.width / 25, self.height // 2 - y))
        #     y += 50
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
