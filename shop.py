import sys

import pygame

import swordsman, archer, cavalry, dragon

import money
from widgets import Button


class Store:
    def __init__(self, screen, size):
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.cell_size = self.main_screen.board.cell_size

        self.lst_units = [swordsman, archer, cavalry, dragon]
        self.lst_products = [('images/team_images/swordsman.png', 25), ('images/team_images/archer.png', 40),
                             ('images/team_images/cavalry.png', 55), ('images/team_images/dragon.png', 120)]

        self.back_button = Button('Назад', round(self.main_screen.board.cell_size * 1.2), round(self.main_screen.board.cell_size * 1.7), self.height - 100,
                                  color=(200, 75, 75), dark_color=(150, 25, 25))

        self.lst_buttons = [self.back_button]

        for i in range(len(self.lst_units)):
            self.buy_btn = Button('Купить', self.cell_size,
                                  i * round(self.cell_size * 4.62) + round(self.cell_size * 4.35),
                                  round(self.cell_size * 9.5), color=(255, 255, 0), dark_color=(0, 255, 0))
            self.lst_buttons.append(self.buy_btn)

        self.fon = pygame.image.load('images/backgrounds/store.png')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def render_products(self):
        for i in range(len(self.lst_units)):
            self.lst_units[i].set_view_stock(self.screen, (
                i * round(self.cell_size * 4.5) + round(self.cell_size * 4.35), round(self.cell_size)), self.cell_size)

        for index in range(len(self.lst_products)):
            im, cost = self.lst_products[index]
            surf = pygame.surface.Surface((round(self.cell_size * 4), round(self.cell_size * 6)))

            image = pygame.image.load(im)
            image = pygame.transform.scale(image, (self.cell_size * 3, self.cell_size * 3))
            image.set_colorkey((0xb3, 0x22, 0xb7))

            font = pygame.font.Font(None, round(self.cell_size * 1.2))
            text = font.render(str(cost), True, 'yellow')

            surf.blit(image, (self.cell_size // 2, 0))
            surf.blit(text, (round(self.cell_size * 1.45), round(self.cell_size * 3.5)))

            money.moneys.draw(self.screen)
            self.main_screen.icon_money.render(self.screen, self.main_screen.money)

            self.screen.blit(surf, (
                index * round(self.cell_size * 4.5) + round(self.cell_size * 2.5), round(self.cell_size * 2.5)))

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
