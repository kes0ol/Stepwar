import pygame
import mapping
import settings


def render(screen, lst):
    lst[0].render(screen)
    lst[1].render(screen)
    lst[2].render(screen)


def check_click(mouse_pos, lst):
    global running
    for button in lst:
        if button.button_rect.left <= mouse_pos[0] <= button.button_rect.right and button.button_rect.top <= mouse_pos[
            1] <= button.button_rect.bottom:
            if button == lst[0]:
                running = False
            if button == lst[1]:
                settings.open()
            if button == lst[2]:
                running = False


def start():
    pygame.display.set_caption('StepWar')

    size = width, height = 1400, 800
    screen = pygame.display.set_mode(size)

    play_game_button = mapping.Button('Запустить игру', 80, 500, height // 2 - 300, 500, height // 2 - 300)
    setting_button = mapping.Button('    Настройки    ', 80, 500, height // 2 - 150, 500, height // 2 - 150)
    exit_button = mapping.Button('        Выйти        ', 80, 500, height // 2, 500, height // 2)
    lst_buttons = [play_game_button, setting_button, exit_button]
    running = True
    fps = 120
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_click(event.pos, lst_buttons)
        screen.fill((0, 0, 0))
        render(screen, lst_buttons)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
