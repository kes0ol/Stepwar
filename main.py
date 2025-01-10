import pygame

import mapping
import start_game
import start_window


class Main:
    def __init__(self):
        self.size = pygame.display.get_desktop_sizes()[0]
        self.screen = mapping.Screen(self.size)
        self.start_screen = start_window.Start_window(self.screen, self.size)

        self.running = True

    def start(self):
        while self.running:
            self.start_screen.start()
            if self.screen.back_to_menu:
                self.start_screen.running = True
                self.start_screen.start()
                self.screen.back_to_menu = False
            if self.screen.gameplay:
                start_game.start(self.screen, self.size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.screen.get_click(event.pos, event.button)

            self.screen.sc.fill((0, 0, 0))
            self.screen.render()

            start_game.show_stats(self.screen)
            clock.tick(fps)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    pygame.mixer.music.load('music/walking.wav')
    pygame.mixer.music.play()
    pygame.time.delay(20)

    fps = 120
    clock = pygame.time.Clock()

    Main().start()
