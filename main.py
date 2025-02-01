import sys

import pygame

import mapping
import start_game
import start_window


class Main:
    def __init__(self):
        self.size = pygame.display.get_desktop_sizes()[-1]
        self.screen = mapping.Screen(self.size, self)

    def go_start_window(self):
        self.start_screen = start_window.Start_window(self.screen, self.size, self)
        self.start_screen.start()

    def start(self, level):
        self.start_screen.running = False
        self.screen.gameplay = False
        self.screen.back_to_menu = False

        self.screen.board.level = level
        self.screen.board.clear_board(self.screen)

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
                        self.screen.back_to_menu = True
                        start_game.return_units()
                        self.screen.board.clear_board(self.screen)
                        self.start_screen.levels_menu.start()
                    elif event.key == pygame.K_SPACE:
                        self.screen.gameplay = True
                    elif event.key == pygame.K_1:
                        self.screen.choose_unit = 'swordsman'
                    elif event.key == pygame.K_2:
                        self.screen.choose_unit = 'archer'
                    elif event.key == pygame.K_3:
                        self.screen.choose_unit = 'cavalry'
                    elif event.key == pygame.K_4:
                        self.screen.choose_unit = 'dragon'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.screen.get_click(event.pos, event.button)

            if self.screen.back_to_menu:
                self.start_screen.start()
                self.screen.back_to_menu = False

            if self.screen.gameplay:
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
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(time_play)
    pygame.time.delay(delay)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    set_music('music/walking.wav', -1, 20)

    main_screen = Main()
    main_screen.go_start_window()
