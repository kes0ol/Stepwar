import sys

import pygame

import mapping

import swordsman, archer, cavalry, dragon

import money
from widgets import Button


class Store(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.lst_units = [swordsman, archer, cavalry, dragon]

        self.lst_products = []
        for i in [('images/team_images/Crusader.png', 25, (0, 0), (100, 100)), ('images/team_images/Sharpshooter.png', 40, (0, 0), (100, 100)),
                  ('images/team_images/Champion.png', 55, (0, 0), (130, 130)), ('images/team_images/bone_dragon.png', 120, (0, 0), (125, 125))]:
            im, cost, ltop, sz = i
            image = pygame.image.load(im)
            image = image.subsurface(pygame.Rect(ltop, sz))
            image = pygame.transform.scale(image, (self.one_size * 3, self.one_size * 3))
            self.lst_products.append((image, cost))

        self.back_button = Button('Назад', round(self.one_size * 1.2),
                                  round(self.one_size * 1.7), self.height - 100,
                                  color=(200, 75, 75), dark_color=(150, 25, 25))

        self.lst_buttons = [self.back_button]

        for i in range(len(self.lst_units)):
            self.buy_btn = Button('Купить', self.one_size,
                                  i * round(self.one_size * 4.62) + round(self.one_size * 4.35),
                                  round(self.one_size * 9.5), color=(255, 255, 0), dark_color=(0, 255, 0))
            self.lst_buttons.append(self.buy_btn)

        self.fon = pygame.image.load('images/backgrounds/store.png')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def render_products(self):
        for i in range(len(self.lst_units)):
            self.lst_units[i].set_view_stock(self.screen, (
                i * round(self.one_size * 4.5) + round(self.one_size * 4.35), round(self.one_size)), self.one_size)

        for index in range(len(self.lst_products)):
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
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                else:
                    select_button = self.lst_products[self.lst_buttons.index(button) - 1]
                    if self.main_screen.money >= select_button[1]:
                        self.main_screen.money -= select_button[1]
                        self.lst_units[self.lst_buttons.index(button) - 1].stock += 1

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
