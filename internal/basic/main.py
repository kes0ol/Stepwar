import os
import sys

import pygame

from internal.basic import mapping
from internal.basic import start_game
from internal.different import global_vars
from internal.different.global_vars import UNIT_ARCHER, UNIT_CAVALRY, UNIT_DRAGON, UNIT_SWORDSMAN, FPS
from internal.windows import final_window
from internal.windows import start_window, enter_nickname


class Main:
    '''Создание основного класса игры'''

    def __init__(self):
        '''Инициализация класса'''
        pygame.init()  # инициализация pygame
        pygame.display.set_caption('StepWar')  # установка названия

        self.size = pygame.display.get_desktop_sizes()[-1]  # получение размеров экрана
        self.screen = mapping.Screen(self.size, self)  # создание основного экрана

        # установка окна ввода никнэйма
        self.nickname_window = enter_nickname.EnterNicknameWindow(self.screen, self.size, self)
        self.start_screen = start_window.Start_window(self.screen, self.size, self)
        self.final_screen = final_window.Final_window(self.screen, self.size, self)

        start_game.set_music(os.path.join('music', 'walking.wav'), -1, 20)  # запуск музыки

    def run(self):
        '''Функция запуска всей игры'''
        self.go_start_window()  # старт начального экрана

    def go_start_window(self):
        '''Функция запуска начального экрана'''
        start_game.set_music('music/walking.wav', -1, 20)
        if not global_vars.current_user:
            self.nickname_window.start()
        self.start_screen.start()

    def go_final_window(self):
        '''Функция запуска финального экрана'''
        start_game.set_music('music/win.mp3', -1, 20)
        self.final_screen.start()

    def start(self, level):
        '''Запуск основного цикла программы'''
        # снос переменных
        self.start_screen.running = False
        self.screen.gameplay = False
        self.screen.back_to_menu = False

        choose_unit = {pygame.K_1: (UNIT_SWORDSMAN, self.screen.icon_swordsman),
                       pygame.K_2: (UNIT_ARCHER, self.screen.icon_archer),
                       pygame.K_3: (UNIT_CAVALRY, self.screen.icon_cavalry),
                       pygame.K_4: (UNIT_DRAGON, self.screen.icon_dragon)}

        self.screen.board.level = level  # загрузка левела
        self.screen.board.clear_board()  # очистка поля

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
                        # выход в меню, очистка поля
                        self.screen.back_to_menu = True
                        start_game.set_music('music/walking.wav', -1, 20)
                        start_game.return_units()
                        self.screen.board.clear_board()
                        self.start_screen.levels_menu.start()
                    elif event.key in choose_unit.keys():
                        self.screen.choose_unit = choose_unit[event.key][0]  # запись выбранного юнита
                        self.screen.choose_unit_surface[1] = [choose_unit[event.key][1].rect.x,  # запись его коорд
                                                              choose_unit[event.key][1].rect.y]

                elif event.type == pygame.MOUSEBUTTONDOWN:  # при нажатии на кнопки мышки
                    self.screen.get_click(event.pos, event.button)

            if self.screen.back_to_menu:  # вернуться назад
                self.start_screen.start()
                self.screen.back_to_menu = False

            elif self.screen.gameplay:  # начать геймплей
                start_game.start(self.screen)
                self.start_screen.levels_menu.start()

            # отображение ресурсов на экране
            self.screen.sc.fill((0, 0, 0))
            self.screen.render()
            self.screen.render_cursor()
            start_game.show_stats(self.screen)
            self.screen.render_cursor()
            clock.tick(FPS)
            pygame.display.flip()

        # выход из игры
        pygame.quit()
        sys.exit()