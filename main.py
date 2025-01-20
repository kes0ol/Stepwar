import pygame

import mapping
import start_game
import start_window


class Main:
    def __init__(self):
        self.size = pygame.display.get_desktop_sizes()[0]
        self.screen = mapping.Screen(self.size, self)

        self.fps = 120
        self.clock = pygame.time.Clock()

        self.running = True

    def go_start_window(self):
        self.start_screen = start_window.Start_window(self.screen, self.size, self)
        self.start_screen.start()

    def start(self, level):
        self.start_screen.running = False
        self.screen.gameplay = False
        self.screen.back_to_menu = False

        self.screen.board.level = level
        self.screen.board.clear_board(self.screen)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.screen.back_to_menu = True
                        self.screen.board.clear_board(self.screen)
                        self.start_screen.levels_menu.start()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.screen.get_click(event.pos, event.button)

            if self.screen.back_to_menu:
                self.start_screen.running = True
                self.start_screen.start()
                self.screen.back_to_menu = False

            if self.screen.gameplay:
                start_game.start(self.screen, self.size)
                self.start_screen.levels_menu.start()

            self.screen.sc.fill((0, 0, 0))
            self.screen.render()

            start_game.show_stats(self.screen)

            self.clock.tick(self.fps)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    pygame.mixer.music.load('music/walking.wav')
    pygame.mixer.music.play(-1)
    pygame.time.delay(20)

    main_screen = Main()
    main_screen.go_start_window()
