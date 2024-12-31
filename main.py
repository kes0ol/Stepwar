import pygame

import mapping
import start_game
import start_window
import pygame as pg
import sys

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')
    pg.mixer.music.load('music/walking.wav')
    pg.mixer.music.play()

    pg.time.delay(20)

    size = 2040, 1160
    main_screen = mapping.Screen(size)
    board = main_screen.board
    button_start_game = main_screen.button_start_game
    back_button = main_screen.back_button

    start_screen = start_window.Start_window(main_screen.sc, size)

    running = True
    fps = 120
    clock = pygame.time.Clock()
    while running:
        start_screen.start()
        if main_screen.board.back_to_menu:
            start_screen.running = True
            start_screen.start()
            main_screen.board.back_to_menu = False
        if board.gameplay:
            start_game.start(main_screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_screen.get_click(event.pos, event.button)
        main_screen.sc.fill((0, 0, 0))
        main_screen.render()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
