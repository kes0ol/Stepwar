import os

import pygame

from development.different import money
from development.different.widgets import Button
from development.units import archer, swordsman, dragon, cavalry
from development.windows import window


class Store(window.Window):
    '''Создание класса страницы магазина'''

    def __init__(self, screen, size, main):
        '''Инициализация класса'''
        super().__init__(screen, size, main, ('images', 'backgrounds', 'store.png'))
        self.screen = pygame.surface.Surface((self.width, self.height))  # создание полотна

        self.lst_units = [swordsman, archer, cavalry, dragon]  # список всех юнитов

        # загрузка всех карточек юнитов в список
        self.lst_products = []
        for i in [(os.path.join('images', 'team_images', 'swordsman.png'), 30, (0, 0), (100, 100)),
                  (os.path.join('images', 'team_images', 'archer.png'), 40, (0, 0), (100, 100)),
                  (os.path.join('images', 'team_images', 'cavalry.png'), 60, (0, 0), (130, 130)),
                  (os.path.join('images', 'team_images', 'dragon.png'), 120, (0, 0), (125, 125))]:
            im, cost, ltop, sz = i
            image = pygame.image.load(im)
            image = image.subsurface(pygame.Rect(ltop, sz))
            image = pygame.transform.scale(image, (self.one_size * 3, self.one_size * 3))
            self.lst_products.append((image, cost))

        self.back_button = Button('Назад', round(self.one_size * 1.2),
                                  round(self.one_size * 1.7), self.height - 100,
                                  color=(200, 75, 75), dark_color=(150, 25, 25))  # создание кнопки Назад

        window.Window.set_lists(self, [self.back_button, ])

        for i in range(len(self.lst_units)):
            self.buy_btn = Button('Купить', self.one_size,
                                  i * round(self.one_size * 4.62) + round(self.one_size * 4.35),
                                  round(self.one_size * 9.5), color=(255, 255, 0),
                                  dark_color=(0, 255, 0))  # создание кнопок Купить
            self.lst_buttons.append(self.buy_btn)

    def render_products(self):
        '''Функция отображение карточек юнитов'''
        for i in range(len(self.lst_units)):  # отображение кол-ва
            self.lst_units[i].set_view_stock(self.screen, (
                i * round(self.one_size * 4.5) + round(self.one_size * 4.35), round(self.one_size)), self.one_size)

        for index in range(len(self.lst_products)):  # отображение самой карточки с кнопкой Купить
            image, cost = self.lst_products[index]
            surf = pygame.surface.Surface((round(self.one_size * 4), round(self.one_size * 6)))

            font = pygame.font.Font(None, round(self.one_size * 1.2))
            text = font.render(str(cost), True, 'yellow')

            surf.blit(image, (self.one_size // 2, 0))
            surf.blit(text, (round(self.one_size * 1.45), round(self.one_size * 3.5)))

            money.moneys.draw(self.screen)
            self.main_screen.icon_money.render(self.screen, self.main_screen.money)

            self.screen.blit(surf, (
                index * round(self.one_size * 4.5) + round(self.one_size * 2.5), round(self.one_size * 2.5)))

    def check_click(self, mouse_pos, lst):
        '''Функция проверки клика мышки'''
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                else:
                    select_button = self.lst_products[self.lst_buttons.index(button) - 1]
                    if self.main_screen.money >= select_button[1]:
                        self.main_screen.money -= select_button[1]
                        self.lst_units[self.lst_buttons.index(button) - 1].stock += 1

    @window.Window.render_decorator
    def render(self):
        '''Рендер всего содержимого магазина'''
        self.render_products()

    @window.Window.start_decoration
    def start(self, event):
        '''Функция старта основного цикла'''
        if event.type == pygame.KEYDOWN:  # при нажатии клавиш
            if event.key == pygame.K_ESCAPE:  # если нажат escape
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # если клик мышки
            self.check_click(event.pos, self.lst_buttons)
