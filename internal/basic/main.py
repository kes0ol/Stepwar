import sys

import pygame

from internal.basic import mapping
from internal.basic import start_game
from internal.different import global_vars
from internal.windows import final_window
from internal.windows import start_window, enter_nickname

from internal.different.global_vars import UNIT_ARCHER, UNIT_CAVALRY, UNIT_DRAGON, UNIT_SWORDSMAN


class Main:
    '''Создание основного класса игры'''

    def __init__(self):
        '''Инициализация класса'''
        pygame.init()  # инициализация pygame
        pygame.display.set_caption('StepWar')  # устновка названия

        self.size = pygame.display.get_desktop_sizes()[-1]  # получение размеров экрана
        self.screen = mapping.Screen(self.size, self)  # создание основного экрана

        self.nickname_window = enter_nickname.EnterNicknameWindow(self.screen, self.size, self)
        self.start_screen = start_window.Start_window(self.screen, self.size, self)
        self.final_screen = final_window.Final_window(self.screen, self.size, self)

        set_music(os.path.join('music', 'walking.wav'), -1, 20)  # запуск музыки

    def run(self):
        self.go_start_window()  # старт начального экрана

    def go_start_window(self):
        if not global_vars.current_user:
            self.nickname_window.start()
        self.start_screen.start()

    def go_final_window(self):
        self.final_screen.start()

    def start(self, level):
        '''Запуск основного цикла программы'''
        self.start_screen.running = False
        self.screen.gameplay = False
        self.screen.back_to_menu = False

        self.screen.board.level = level
        self.screen.board.clear_board()  # очистка поля

        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:  # запуск основного цикла
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # проверка на выход
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:  # при нажатии на клавиши
                    if event.key == pygame.K_ESCAPE:  # если нажат escape
                        self.screen.back_to_menu = True
                        start_game.return_units()
                        self.screen.board.clear_board()
                        self.start_screen.levels_menu.start()
                    elif event.key == pygame.K_1:  # если нажата клавиша 1
                        self.screen.choose_unit = UNIT_SWORDSMAN
                        self.screen.choose_unit_surface[1] = [self.screen.icon_swordsman.rect.x,
                                                              self.screen.icon_swordsman.rect.y]
                    elif event.key == pygame.K_2:  # если нажата клавиша 2
                        self.screen.choose_unit = UNIT_ARCHER
                        self.screen.choose_unit_surface[1] = [self.screen.icon_archer.rect.x,
                                                              self.screen.icon_archer.rect.y]
                    elif event.key == pygame.K_3:  # если нажата клавиша 3
                        self.screen.choose_unit = UNIT_CAVALRY
                        self.screen.choose_unit_surface[1] = [self.screen.icon_cavalry.rect.x,
                                                              self.screen.icon_cavalry.rect.y]
                    elif event.key == pygame.K_4:  # если нажата клавиша 4
                        self.screen.choose_unit = UNIT_DRAGON
                        self.screen.choose_unit_surface[1] = [self.screen.icon_dragon.rect.x,
                                                              self.screen.icon_dragon.rect.y]

                if event.type == pygame.MOUSEBUTTONDOWN:  # при нажатии на кнопки мышки
                    self.screen.get_click(event.pos, event.button)

            if self.screen.back_to_menu:  # вернуться назад
                self.start_screen.start()
                self.screen.back_to_menu = False

            if self.screen.gameplay:  # начать геймплей
                start_game.start(self.screen)
                self.start_screen.levels_menu.start()

            self.screen.sc.fill((0, 0, 0))
            self.screen.render()
            self.screen.render_cursor()
            start_game.show_stats(self.screen)
            self.screen.render_cursor()
            clock.tick(fps)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def set_music(path, time_play, delay):
    '''Функция задания музыки'''
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(time_play)
    pygame.time.delay(delay)
