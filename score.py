import sys

import pygame

import mapping

from widgets import Button


class Score_window(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.volume = 1
        self.screen = pygame.surface.Surface((self.width, self.height))

        self.back_button = Button('Назад', self.one_size, self.one_size * 2, self.one_size * 11, color=(150, 0, 0),
                                  dark_color=(100, 0, 0))

        self.lst_buttons = [self.back_button]

        self.fon = pygame.image.load('images/backgrounds/score.PNG')
        self.fon = pygame.transform.scale(self.fon, (self.size[0], self.size[1]))

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False

    def render(self):
        self.screen.blit(self.fon, (0, 0))
        for button in self.lst_buttons:
            button.render(self.screen)
        self.main_screen.sc.blit(self.screen, (0, 0))
        pygame.draw.rect(self.main_screen.sc, (0, 0, 0), (self.width / 5, self.height / 2.5,
                                                          self.one_size * 12, self.one_size * 6), 8)
        pygame.draw.rect(self.main_screen.sc, (0, 0, 0), (self.one_size * 8.1, self.height / 2.5,
                                                          self.one_size * 4.3, self.one_size * 6), 8)
        f = pygame.font.Font(None, 100)
        t = f.render('Лучшие результаты', True, 'red')
        self.main_screen.sc.blit(t, (self.one_size * 7, self.one_size * 2))
        f1 = pygame.font.Font(None, 100)
        t1 = f1.render('lvl 1', True, 'red')
        self.main_screen.sc.blit(t1, (self.one_size * 5.5, self.one_size * 4))
        f2 = pygame.font.Font(None, 100)
        t2 = f2.render('lvl 2', True, 'red')
        self.main_screen.sc.blit(t2, (self.one_size * 9.5, self.one_size * 4))
        f3 = pygame.font.Font(None, 100)
        t3 = f3.render('lvl 3', True, 'red')
        self.main_screen.sc.blit(t3, (self.one_size * 13.5, self.one_size * 4))
        self.main_screen.render_cursor()


    def start(self):
        fps = 60
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
