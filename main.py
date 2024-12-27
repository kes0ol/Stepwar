import pygame

import mapping

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    size = 1400, 800
    screen1 = mapping.Screen(size)
    board = mapping.Board(18, 10, size)

    rect_width, rect_height = 200, 26
    button_start_game = mapping.Button(size, 38, 200, 26, 1100, 700, rect_width, rect_height)

    running = True
    fps = 120
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos, event.button)
        screen1.sc.fill((0, 0, 0))
        screen1.render(board, button_start_game, rect_width, rect_height)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
