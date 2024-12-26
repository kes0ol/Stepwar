import pygame

import mapping

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    size = 1400, 800
    screen1 = mapping.Screen(size)
    board = mapping.Board(18, 11, size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen1.sc.fill((0, 0, 0))
        screen1.render(board)
        pygame.display.flip()
    pygame.quit()
