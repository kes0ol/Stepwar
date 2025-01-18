import sys

import pygame

import swordsman, archer, cavalry, dragon

import money
from global_vars import FILL_TYPE_BORDER
from widgets import Button, View


class Store:
    def __init__(self, screen, size):
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.back_button = Button('Назад', 80, 120, self.height - 100, color=(200, 75, 75), dark_color=(150, 25, 25))
        self.buy_sw = Button('Купить', 80, 300, self.height - 250, color=(255, 255, 0),
                             dark_color=(0, 255, 0))
        self.buy_ar = Button('Купить', 80, 600, self.height - 250, color=(255, 255, 0),
                             dark_color=(0, 255, 0))
        self.buy_cav = Button('Купить', 80, 900, self.height - 250, color=(255, 255, 0),
                              dark_color=(0, 255, 0))
        self.buy_dr = Button('Купить', 80, 1200, self.height - 250, color=(255, 255, 0),
                             dark_color=(0, 255, 0))
        self.lst_buttons = [self.back_button, self.buy_sw, self.buy_ar, self.buy_cav, self.buy_dr]

        self.fon = pygame.image.load('images/backgrounds/store.png')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

        self.lst_products = [('images/team_images/swordsman.png', 25), ('images/team_images/archer.png', 40),
                             ('images/team_images/cavalry.png', 55), ('images/team_images/dragon.png', 120)]

    def render_products(self):
        swordsman.set_view_stock(self.screen, (300, 150), 50)
        archer.set_view_stock(self.screen, (600, 150), 50)
        cavalry.set_view_stock(self.screen, (900, 150), 50)
        dragon.set_view_stock(self.screen, (1200, 150), 50)

        for index in range(len(self.lst_products)):
            im, cost = self.lst_products[index]
            surf = pygame.surface.Surface((200, 300))

            image = pygame.image.load(im)
            image = pygame.transform.scale(image, (200, 200))
            image.set_colorkey((0xb3, 0x22, 0xb7))

            font = pygame.font.Font(None, 40)
            text = font.render(str(cost), True, 'yellow')

            surf.blit(image, (0, 0))
            surf.blit(text, (90, 250))

            money.moneys.draw(self.screen)
            self.main_screen.icon_money.render(self.screen, self.main_screen.money)

            self.screen.blit(surf, (index * 300 + 200, 200))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                if button == self.buy_sw:
                    if self.main_screen.money >= self.lst_products[0][1]:
                        self.main_screen.money -= self.lst_products[0][1]
                        swordsman.stock += 1
                if button == self.buy_ar:
                    if self.main_screen.money >= self.lst_products[1][1]:
                        self.main_screen.money -= self.lst_products[1][1]
                        archer.stock += 1
                if button == self.buy_cav:
                    if self.main_screen.money >= self.lst_products[2][1]:
                        self.main_screen.money -= self.lst_products[2][1]
                        cavalry.stock += 1
                if button == self.buy_dr:
                    if self.main_screen.money >= self.lst_products[3][1]:
                        self.main_screen.money -= self.lst_products[3][1]
                        dragon.stock += 1

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        self.render_products()
        for button in self.lst_buttons:
            button.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))
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

            self.screen.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
