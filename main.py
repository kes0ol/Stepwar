import pygame

import board
import swordsman
import castle

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')
    size = width, height = 1400, 800
    screen = pygame.display.set_mode(size)
    board = board.Board(18, 11)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        castle.castles.draw(screen)
        swordsman.swordsmans.draw(screen)
        pygame.display.flip()
    pygame.quit()
