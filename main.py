import pygame

import mapping
import start_game

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    size = 1400, 800
    screen = mapping.Screen(size)
    board = screen.board

    running = True
    fps = 120
    clock = pygame.time.Clock()
    while running:
        if board.gameplay:
            start_game.start(screen)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.get_click(event.pos, event.button)
        screen.sc.fill((0, 0, 0))
        screen.render()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
