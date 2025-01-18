import sys

import pygame

import archer
import castle
import cavalry
import dragon

from widgets import Button

import swordsman


class Reference_Window:
    def __init__(self, screen, size, main):
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.swordsman_button = Button('Рыцарь', 100, self.width // 10, self.height // 10, color=(100, 0, 0),
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
        self.icon_unit = None

        self.fon = pygame.image.load('images/backgrounds/reffon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

        self.stats = []

    def check_click(self, mouse_pos, lst):
        self.icons_units.empty()
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.swordsman_button:
                    self.icon_unit = swordsman.Swordsman(self.width / 1.35, self.height // 2, 500, self.icons_units)
                    self.stats = [
                        f'Тип юнита: Рыцарь',
                        f'Здоровье: {self.icon_unit.hp}',
                        f'Урон: {self.icon_unit.damage}',
                        f'Передвижение: {self.icon_unit.step}',
                        f'Дистанция атаки: {self.icon_unit.distance_attack}']
                if button == self.archer_button:
                    self.icon_unit = archer.Archer(self.width / 1.35, self.height // 2, 500, self.icons_units)
                    self.stats = [
                        f'Тип юнита: Лучник',
                        f'Здоровье: {self.icon_unit.hp}',
                        f'Урон: {self.icon_unit.damage}',
                        f'Передвижение: {self.icon_unit.step}',
                        f'Дистанция атаки: {self.icon_unit.distance_attack}']
                if button == self.dragon_button:
                    self.icon_unit = dragon.Dragon(self.width / 1.35, self.height // 2, 200, self.icons_units)
                    self.stats = [
                        f'Тип юнита: Дракон',
                        f'Здоровье: {self.icon_unit.hp}',
                        f'Урон: {self.icon_unit.damage}',
                        f'Передвижение: {self.icon_unit.step}',
                        f'Дистанция атаки: {self.icon_unit.distance_attack}']
                if button == self.cavalry_button:
                    self.icon_unit = cavalry.Cavalry(self.width / 1.35, self.height // 2, 200, self.icons_units)
                    self.stats = [
                        f'Тип юнита: Кавалерия',
                        f'Здоровье: {self.icon_unit.hp}',
                        f'Урон: {self.icon_unit.damage}',
                        f'Передвижение: {self.icon_unit.step}',
                        f'Дистанция атаки: {self.icon_unit.distance_attack}']
                if button == self.castle_button:
                    self.icon_unit = castle.Castle(self.width / 1.35, self.height // 2, 200, self.icons_units)
                    self.stats = [
                        f'Тип юнита: Замок',
                        f'Здоровье: {self.icon_unit.hp}',
                        f'Урон: {self.icon_unit.damage}',
                        f'Передвижение: {self.icon_unit.step}',
                        f'Дистанция атаки: {self.icon_unit.distance_attack}']
                if button == self.back_button:
                    self.running = False

    def render(self):
        y = 50

        self.main_screen.sc.blit(self.fon, (0, 0))
        self.icons_units.draw(self.main_screen.sc)

        for i in reversed(self.stats):
            font = pygame.font.Font(None, 40)
            text = font.render(i, True, 'black')
            self.main_screen.sc.blit(text, (self.width / 1.8, self.height // 2 - y))
            y += 50
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.render_cursor()

    def start(self):
        self.running = True
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
