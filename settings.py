import pygame
import mapping

def check_click(mouse_pos, lst):
    global running_settings
    for button in lst:
        if button.button_rect.left <= mouse_pos[0] <= button.button_rect.right and button.button_rect.top <= mouse_pos[
            1] <= button.button_rect.bottom:
            if button == lst[7]:
                running_settings = False


def render(screen, lst):
    lst[0].render(screen)
    lst[1].render(screen)
    lst[2].render(screen)
    lst[3].render(screen)
    lst[4].render(screen)
    lst[5].render(screen)
    lst[6].render(screen)
    lst[7].render(screen)
    pygame.draw.rect(screen, pygame.Color('green'), pygame.Rect(180, 160, 970, 100), 1)

def open():
    pygame.display.set_caption('Settings')

    size = width, height = 1400, 800
    screen = pygame.display.set_mode(size)

    volume_button = mapping.Button('  Громкость  ', 80, 500, height // 2 - 320, 500, height // 2 - 320)
    off_volume_button = mapping.Button('  Turn off  ', 50, 200, height // 2 - 200, 200, height // 2 - 200)
    twenty_volume_button = mapping.Button('  20%  ', 50, 400, height // 2 - 200, 400, height // 2 - 200)
    fourty_volume_button = mapping.Button('  40%  ', 50, 550, height // 2 - 200, 550, height // 2 - 200)
    sixty_volume_button = mapping.Button('  60%  ', 50, 700, height // 2 - 200, 700, height // 2 - 200)
    eighty_volume_button = mapping.Button('  80%  ', 50, 850, height // 2 - 200, 850, height // 2 - 200)
    hundred_volume_button = mapping.Button('  100%  ', 50, 1000, height // 2 - 200, 1000, height // 2 - 200)
    back_button = mapping.Button('      Назад      ', 80, 500, height // 2, 500, height // 2)
    lst_buttons = [volume_button, off_volume_button, twenty_volume_button, fourty_volume_button, sixty_volume_button,
                   eighty_volume_button, hundred_volume_button, back_button]
    running_settings = True
    fps = 120
    clock = pygame.time.Clock()
    while running_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_settings = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_click(event.pos, lst_buttons)
        screen.fill((0, 0, 0))
        render(screen, lst_buttons)
        clock.tick(fps)
        pygame.display.flip()







