import pygame

import os
import sys


class Window:
    '''Родительский класс окон'''

    def __init__(self, screen, size, main, fon_path):
        '''Инициализация класа'''
        self.size = self.width, self.height = size
        self.main_screen = screen
        self.main = main

        self.screen = pygame.surface.Surface((self.width, self.height))

        self.fon = pygame.image.load(os.path.join(*fon_path))
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

        self.one_size = self.main_screen.board.cell_size

    def parse_text(self, text, width):
        '''Функция парсинга текста'''
        lst = text.split()
        res = []
        w = width
        st = ''
        while len(lst) > 1:
            while w > 0 and len(lst) > 1:
                if len(lst[0]) > 0:
                    st += lst[0] + ' '
                    lst = lst[1:]
                    w -= len(lst[0])
                else:
                    break
            w = width
            res.append(st)
            st = ''
        return res

    def set_lists(self, lst_buttons=(), lst_views=()):
        self.lst_buttons = list(lst_buttons)
        self.lst_views = list(lst_views)

    def render_decorator(func):
        '''Декоратор функции рендера экрана'''

        def wrapper(*args):
            self = args[0]
            self.screen.blit(self.fon, (0, 0))

            func(*args)

            for button in self.lst_buttons:
                button.render(self.screen)
            for view in self.lst_views:
                view.render(self.screen)

            self.main_screen.sc.blit(self.screen, (0, 0))
            self.main_screen.render_cursor()

        return wrapper

    def start_decoration(func):
        '''Декоратор функции старта цикла экрана'''

        def wrapper(*args):
            self = args[0]

            fps = 60
            clock = pygame.time.Clock()

            self.running = True
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        sys.exit()

                    func(*args, event)

                self.screen.fill((0, 0, 0))
                self.render()

                clock.tick(fps)
                pygame.display.flip()

        return wrapper
