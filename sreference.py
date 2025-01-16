import sys

import pygame
import settings
import levels
from widgets import Button

import swordsman


class Reference_Window:
    def __init__(self, screen, size, main):
        self.running = True
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.swordsman_button = Button('Мечник', 100, self.width // 10, self.height // 10, color=(100, 0, 0),
                                       dark_color=(50, 0, 0))
        self.archer_button = Button('Лучник', 100, self.width // 10, self.height / 5.3, color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.cavalry_button = Button('Кавалерия', 100, self.width // 10, self.height / 3.8, color=(100, 0, 0),
                                     dark_color=(50, 0, 0))
        self.dragon_button = Button('Дракон', 100, self.width // 10, self.height / 2.7, color=(100, 0, 0),
                                    dark_color=(50, 0, 0))

        self.castle_button = Button('Замок', 100, self.width // 10, self.height / 2, color=(100, 0, 0),
                                    dark_color=(50, 0, 0))

        self.back_button = Button('<-', 200, 80, self.height - 80,
                                  color=(100, 0, 0), dark_color=(50, 0, 0))

        self.grass_button = Button('Трава', 100, self.width / 3.5, self.height / 10, color=(100, 0, 0),
                                   dark_color=(50, 0, 0))
        self.rock_button = Button('Гора', 100, self.width / 3.5, self.height / 5.3, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.hill_button = Button('Холм', 100, self.width / 3.5, self.height / 3.8, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.river_button = Button('Река', 100, self.width / 3.5, self.height / 2.7, color=(100, 0, 0),
                                   dark_color=(50, 0, 0))

        self.lst_buttons = [self.back_button, self.swordsman_button, self.archer_button, self.cavalry_button,
                            self.dragon_button, self.castle_button, self.grass_button, self.rock_button,
                            self.hill_button, self.river_button]

        self.icons_units = pygame.sprite.Group()
        self.icon_sw = swordsman.Swordsman(200,200, 500, self.icons_units)

        self.fon = pygame.image.load('images/reffon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))


    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.swordsman_button:
                    self.type_of_unit = 'Мечник'
                    self.damage = self.icon_sw.damage
                if button == self.back_button:
                    self.running = False

    def render(self):
        self.main_screen.sc.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.render_cursor()

        self.icons_units.draw(self.main_screen.sc)

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
