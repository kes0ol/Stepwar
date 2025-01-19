import sys

import pygame
import sreference
from widgets import Button


class Reference_window:
    def __init__(self, screen, size, main):
        self.running = True
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.next_page_button = Button('->', 200, self.width - 80, self.height - 80,
                                  color=(100, 0, 0), dark_color=(50, 0, 0))
        self.back_button = Button('Назад в Главное меню', 80, self.width // 2, self.height // 2 + 200,
                                  color=(100, 0, 0), dark_color=(50, 0, 0))
        self.lst_buttons = [self.back_button, self.next_page_button]

        self.lst = ['Каждый юнит обладает уникальными характеристиками, такие как: урон, дальность атаки, дальность передвижения и другими атрибутами.',
                    'После расстановки юнитов нажмите "Начать игру" и управляйте своими юнитами, а так же пробуйте вступать в схватку с противником.',
                    'Перед тем как начать игру, вы можете расставить своих юнитов, нажимая на иконку слева от поля битвы и кликая на клетку поля.',
                    'Игровой процесс.',
                    'За пройденный уровень вы получаете очки. Чтобы пройти уровень, нужно сокрушить вражеский замок.',
                    'Игра представляет собой стратегию, состоящая из уровней. С каждым открытым уровнем вы получаете доступ к следующему.']

        self.fon = pygame.image.load('images/backgrounds/reffon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

        self.ref_screen = sreference.Reference_Window(self.main_screen, self.size, self.main)

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.next_page_button:
                    self.ref_screen.start()
                if button == self.back_button:
                    self.running = False
                    self.main.go_start_window()


    def render(self):
        y = 50
        self.main_screen.sc.blit(self.fon, (0, 0))
        for i in self.lst:
            font = pygame.font.Font(None, 40)
            text = font.render(i, True, 'black')
            self.main_screen.sc.blit(text, (self.width / 25, self.height // 2 - y))
            y += 50
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
