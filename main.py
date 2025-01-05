import pygame

import mapping
import start_game
import start_window

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('StepWar')

    SIZE = pygame.display.get_desktop_sizes()[0]

    pygame.mixer.music.load('music/walking.wav')
    pygame.mixer.music.play()
    pygame.time.delay(20)

    main_screen = mapping.Screen(SIZE)
    board = main_screen.board

    start_screen = start_window.Start_window(main_screen, SIZE)

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
            start_game.start(main_screen, SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_screen.get_click(event.pos, event.button)

        main_screen.sc.fill((0, 0, 0))
        main_screen.render()
        start_game.show_stats(main_screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
