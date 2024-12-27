import pygame

import mapping
import start_game

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    size = 1400, 800
    screen1 = mapping.Screen(size)
    board = screen1.board

    button_start_game = screen1.button_start_game

    running = True
    fps = 120
    clock = pygame.time.Clock()
    while running:
        if button_start_game.gameplay:
            start_game.start(screen1)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen1.get_click(event.pos, event.button)
        screen1.sc.fill((0, 0, 0))
        screen1.render(board, button_start_game)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
