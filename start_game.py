import itertools
import random
import sys

import pygame

import swordsman, archer, cavalry, dragon
import landscapes
from global_vars import my_units_group, enemies_group, RANGE_ATTACK, shop_group, action_in_progress, landscape_group

is_win = None
money_now = 0


def start(screen):
    global is_win, money_now
    # enemys_move(screen)
    money_now = 0

    fps = 60
    clock = pygame.time.Clock()
    running = True
    while screen.gameplay and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not action_in_progress:
                        running = False
                        return_units()
                        new_step()
                        screen.board.clear_board(screen)
                if event.key == pygame.K_SPACE:
                    if not action_in_progress:
                        screen.steps += 1
                        new_step()
                        enemys_move(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                select_button = check_click(screen, event.pos)
                if select_button == 'new_step':
                    if not action_in_progress:
                        screen.steps += 1
                        new_step()
                        enemys_move(screen)
                if select_button == 'back_to_menu':
                    if not action_in_progress:
                        running = False
                        return_units()
                        new_step()
                        screen.board.clear_board(screen)
                if screen.setting_button.check_click(event.pos):
                    screen.main.start_screen.settings_screen.start()
                if screen.ref_button.check_click(event.pos):
                    screen.main.start_screen.ref_screen.start()

                cell_coords = screen.board.get_cell(event.pos)
                unit = choose_unit(screen, cell_coords)
                if unit is not None and event.button == 1:
                    choose_step(screen, unit, cell_coords)
                if unit is not None and event.button == 3:
                    choose_attack(screen, unit, cell_coords)

        screen.sc.fill((0, 0, 0))
        screen.render()
        screen.render_cursor()
        show_stats(screen)
        clock.tick(fps)
        pygame.display.flip()


def end(screen):
    global money_now
    screen.money += money_now
    surf = pygame.Surface((screen.board.cell_size * 8, screen.board.cell_size * 4))

    fps = 60
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not action_in_progress:
                        running = False
                        screen.gameplay = False
                        return_units()
                        new_step()
                        screen.board.clear_board(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                select_button = check_click(screen, event.pos)

                if select_button == 'back_to_menu':
                    if not action_in_progress:
                        running = False
                        screen.gameplay = False
                        return_units()
                        new_step()
                        screen.board.clear_board(screen)
                if screen.setting_button.check_click(event.pos):
                    screen.main.start_screen.settings_screen.start()
                if screen.ref_button.check_click(event.pos):
                    screen.main.start_screen.ref_screen.start()

        screen.sc.fill((0, 0, 0))
        screen.render()
        show_stats(screen)
        draw_end_surface(screen, surf)
        screen.render_cursor()
        clock.tick(fps)
        pygame.display.flip()


def draw_end_surface(screen, main_surf):
    global money_now
    one_size = screen.board.cell_size
    lst = []

    surf = pygame.surface.Surface((one_size * 6, one_size * 2))

    surf.fill('white')
    main_surf.fill('black')

    if is_win:
        font = pygame.font.Font(None, round(one_size * 1.4))
        text = font.render('Вы победили!', True, 'white')
    else:
        font = pygame.font.Font(None, round(one_size * 1.3))
        text = font.render('Вас уничтожили!', True, 'white')
    main_surf.blit(text, (one_size // 5, one_size // 5))

    lst.append((f'Заработанные монеты: {money_now}', one_size // 2))
    lst.append((f'Счёт: {screen.score * (20 // screen.steps)}', one_size // 2))

    for i in range(len(lst)):
        font = pygame.font.Font(None, lst[i][1])
        text = font.render(lst[i][0], True, 'black')
        surf.blit(text, (10, i * 50 + 20))

    main_surf.blit(surf, (one_size, one_size * 1.5))
    screen.sc.blit(main_surf, (one_size * 8, one_size * 4))


def return_units():
    for unit in my_units_group:
        if unit.name == "swordsman":
            swordsman.stock += 1
        if unit.name == "archer":
            archer.stock += 1
        if unit.name == "cavalry":
            cavalry.stock += 1
        if unit.name == "dragon":
            dragon.stock += 1


def check_borders(board, cell_x, cell_y, dx, dy):
    return ((dx, dy) != (0, 0) and
            0 <= cell_x + dx < len(board.board[0]) and
            0 <= cell_y + dy < len(board.board))


def enemys_move(screen):
    for unit in enemies_group:
        if unit.step == 0:
            continue

        cell = screen.board.get_cell((unit.rect.x, unit.rect.y))
        lst_steps, _ = select_surfaces(screen.board, unit, cell, False)

        if len(lst_steps):
            choise_cell = random.choice(lst_steps)

            # if screen.board.board[choise_cell[1]][choise_cell[0]] == 0 and cell != (-1, -1):
            increment_action_in_progress()
            unit.make_step(cell, choise_cell, screen, enemys_attack, [screen, unit, choise_cell])


def show_stats(screen):
    stats_surface = pygame.Surface((200, 100))
    font = pygame.font.Font(None, 25)
    stats = []

    for un in itertools.chain(enemies_group, my_units_group, shop_group):
        if un.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: {un.title}',
                f'Здоровье: {un.hp}',
                f'Урон: {un.damage}' + (f' + {un.damage_plus}' if un.attack_type == RANGE_ATTACK else ''),
                f'Передвижение: {un.step}',
                f'Дистанция атаки: {un.distance_attack}'
            ]

    if len(stats) == 0:
        for land in landscape_group:
            if land.rect.collidepoint(pygame.mouse.get_pos()):
                stats = [
                    f'Ландшафт: {land.title}',
                    f'Доп. урон: {land.damage}',
                    f'Передвижение: {land.move}'
                ]

    for i in range(len(stats)):
        text = font.render(stats[i], True, (255, 255, 255))
        stats_surface.blit(text, (0, i * 20, 100, 100))
    screen.sc.blit(stats_surface, (screen.board.left // 2 - 100, screen.height // 2))


def check_click(screen, mouse_pos):
    if (screen.button_next_step.rect.left <= mouse_pos[0] <= screen.button_next_step.rect.right
            and screen.button_next_step.rect.top <= mouse_pos[1] <= screen.button_next_step.rect.bottom):
        return 'new_step'
    if (screen.back_button.rect.left <= mouse_pos[0] <= screen.back_button.rect.right
            and screen.back_button.rect.top <= mouse_pos[1] <= screen.back_button.rect.bottom):
        return 'back_to_menu'


def choose_unit(screen, cell_coords):
    cell_x, cell_y = cell_coords
    coords = cell_x * screen.board.cell_size + screen.board.left, cell_y * screen.board.cell_size + screen.board.top

    for unit in my_units_group:
        if unit.rect.collidepoint(coords):
            return unit

    return None


def choose_step(screen, unit, cell_coords):
    # is_attack = False
    # lst_surfaces = []
    lst_steps, lst_surfaces = select_surfaces(screen.board, unit, cell_coords, False)
    if unit.step > 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choose_cell = screen.board.get_cell(event.pos)
                    for coords in lst_steps:
                        if coords == choose_cell:
                            increment_action_in_progress()
                            unit.make_step(cell_coords, choose_cell, screen, decrement_action_in_progress, [])
                    return

            screen.sc.fill((0, 0, 0))
            screen.render()
            render_surfaces(screen, lst_surfaces, (0, 200, 0))  # TBD Move to main render view
            show_stats(screen)
            screen.render_cursor()
            pygame.display.flip()


def increment_action_in_progress():
    global action_in_progress
    action_in_progress += 1


class BadActionInProgressState(Exception):
    pass


def decrement_action_in_progress():
    global action_in_progress
    action_in_progress -= 1
    if action_in_progress < 0:
        raise BadActionInProgressState()


def choose_attack(screen, unit, cell_coords):
    # lst_surfaces = []
    lst_steps, lst_surfaces = select_surfaces(screen.board, unit, cell_coords, True)
    if unit.do_damage:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choose_cell = screen.board.get_cell(event.pos)
                    for coords in lst_steps:
                        if coords == choose_cell:
                            increment_action_in_progress()
                            unit.make_attack(choose_cell, screen, decrement_action_in_progress, [])
                    return

            screen.sc.fill((0, 0, 0))
            screen.render()
            render_surfaces(screen, lst_surfaces, (200, 0, 0))
            show_stats(screen)
            screen.render_cursor()
            pygame.display.flip()


def new_step():
    for unit in itertools.chain(my_units_group, enemies_group):
        unit.refresh()


def render_surfaces(screen, lst_surfaces, color):
    for surf in lst_surfaces:
        surface, surface_coords, surface_size = surf
        surface.fill(color)
        surface.set_alpha(60)
        screen.sc.blit(surface, surface_coords)


def enemys_attack(screen, unit, now_cell):
    decrement_action_in_progress()
    lst_steps, _ = select_surfaces(screen.board, unit, now_cell, True)
    if len(lst_steps):
        select_attack = random.choice(lst_steps)

        increment_action_in_progress()
        unit.make_attack(select_attack, screen, decrement_action_in_progress, [])


def give_damage(screen, select_coords, select_cell, actor):
    global is_win, money_now

    for group in [my_units_group, enemies_group]:
        for unit in group:
            if actor in my_units_group:
                target = 3
            if actor in enemies_group:
                target = 4
            if screen.board.board[select_cell[1]][select_cell[0]] == target:
                unit.recieve_damage(actor)
                if unit.is_dead:
                    for i in range(len(screen.board.board)):
                        for j in range(len(screen.board.board[i])):
                            if screen.board.board[i][j] == target:
                                screen.board.board[i][j] = 0
                    if actor in my_units_group:
                        money_now += 100
                        is_win = True
                        screen.progress.add(screen.board.level + 1)
                        end(screen)
                    if actor in enemies_group:
                        is_win = False
                        end(screen)
                    return
            if (unit.rect.x, unit.rect.y) == select_coords:
                unit.recieve_damage(actor)
                if unit.is_dead:
                    screen.board.board[select_cell[1]][select_cell[0]] = 0

                    if actor in my_units_group:
                        if unit.name == 'swordsman':
                            money_now += 10
                            screen.score += 5
                        if unit.name == 'archer':
                            money_now += 15
                            screen.score += 25
                        if unit.name == 'cavalry':
                            money_now += 20
                            screen.score += 20
                        if unit.name == 'dragon':
                            money_now += 50
                            screen.score += 40
                return


def select_surfaces(board, unit, cell, is_attack):
    lst_surfaces = []
    lst_steps = []
    if not is_attack:
        def add(ran, cell_coords):
            cell_x, cell_y = cell_coords

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    minus = 1
                    if abs(dx) != abs(dy):
                        if check_borders(board, cell_x, cell_y, dx, dy):
                            if ((board.board[cell_y + dy][cell_x + dx] == 0 and
                                 board.field[cell_y + dy][cell_x + dx] != 1)):
                                if board.field[cell_y + dy][cell_x + dx] != 3 or \
                                        board.field[cell_y + dy][cell_x + dx] == 3 and unit.name == 'dragon':
                                    if (cell_x + dx, cell_y + dy) not in lst_steps:
                                        lst_steps.append((cell_x + dx, cell_y + dy))

                                        coords = board.get_cell_coords((cell_x + dx, cell_y + dy))
                                        surface = pygame.surface.Surface((board.cell_size, board.cell_size))
                                        lst_surfaces.append((surface, coords, (board.cell_size, board.cell_size)))
                                    if unit.name != 'dragon':
                                        if board.field[cell_y + dy][cell_x + dx] == 2:
                                            minus += 1
                                    if ran - minus > 0:
                                        add(ran - minus, (cell_x + dx, cell_y + dy))

        add(unit.step, cell)
    else:
        if unit in my_units_group:
            enemies = (2, 3)
        else:
            enemies = (1, 4)
        cell_x, cell_y = cell
        for dx in range(-unit.distance_attack, unit.distance_attack + 1):
            for dy in range(-unit.distance_attack, unit.distance_attack + 1):
                if check_borders(board, cell_x, cell_y, dx, dy):
                    if board.board[cell_y + dy][cell_x + dx] in enemies:
                        lst_steps.append((cell_x + dx, cell_y + dy))

                        coords = board.get_cell_coords((cell_x + dx, cell_y + dy))
                        surface = pygame.surface.Surface((board.cell_size, board.cell_size))
                        lst_surfaces.append((surface, coords, (board.cell_size, board.cell_size)))
    return lst_steps, lst_surfaces
