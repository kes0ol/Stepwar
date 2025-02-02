import pygame

import itertools
import random
import sys

from development.units import swordsman, archer, cavalry, dragon

from development.different.global_vars import my_units_group, enemies_group, RANGE_ATTACK, shop_group, \
    landscape_group, action_in_progress

'''Создание глобальных переменных'''
is_win = None
money_now = 0


def start(screen):
    '''Функция старта главноого цикла геймплея'''
    global is_win, money_now  # вызов глобальных переменных

    enemys_move(screen)  # первый ход юнитов
    money_now = 0

    fps = 60
    clock = pygame.time.Clock()
    running = True
    '''Старт цикла'''
    while screen.gameplay and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # проверка выхода
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # при нажатии кнопки
                if event.key == pygame.K_ESCAPE and not action_in_progress:  # нажатие escape (назад)
                    running = False
                    screen.gameplay = False
                    return_units()
                    new_step()
                    screen.board.clear_board()
                if event.key == pygame.K_SPACE and not action_in_progress:  # нажатие пробела (новый ход)
                    screen.steps += 1
                    new_step()
                    enemys_move(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:  # при нажатии мышкой
                select_button = check_click(screen, event.pos)
                if select_button == 'new_step' and not action_in_progress:  # нажатие на кнопку след. хода
                    screen.steps += 1
                    new_step()
                    enemys_move(screen)
                if select_button == 'back_to_menu' and not action_in_progress:  # нажатие на кнопку 'назад'
                    running = False
                    screen.gameplay = False
                    return_units()
                    new_step()
                    screen.board.clear_board()

                if screen.setting_button.check_click(event.pos):  # кнопка настроек
                    screen.main.start_screen.settings_screen.start()
                if screen.ref_button.check_click(event.pos):  # кнопка справки
                    screen.main.start_screen.ref_screen.start()

                cell_coords = screen.board.get_cell(event.pos)
                unit = choose_unit(screen, cell_coords)
                if not action_in_progress:
                    if unit and event.button == 1:  # ЛКМ по персонажам
                        choose_step(screen, unit, cell_coords)
                    if unit and event.button == 3:  # ПКМ по персонажам
                        choose_attack(screen, unit, cell_coords)

        screen.sc.fill((0, 0, 0))
        screen.render()
        screen.render_cursor()
        show_stats(screen)
        clock.tick(fps)
        pygame.display.flip()


def end(screen):
    '''Финальное окно со счётом и зараотанными монетами'''
    global money_now

    screen.money += money_now
    surf = pygame.Surface((screen.board.cell_size * 8, screen.board.cell_size * 4))

    fps = 60
    clock = pygame.time.Clock()

    running = True
    '''Старт цикла экрана'''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # проверка на выход
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # проверка на нажатие клавиш
                if event.key == pygame.K_ESCAPE and not action_in_progress:  # при нажатии на escape
                    running = False
                    screen.gameplay = False
                    return_units()
                    new_step()
                    screen.board.clear_board()

            if event.type == pygame.MOUSEBUTTONDOWN:  # при нажати мышкой
                select_button = check_click(screen, event.pos)

                if select_button == 'back_to_menu' and not action_in_progress:  # нажатие кнопки 'назад'
                    running = False
                    screen.gameplay = False
                    return_units()
                    new_step()
                    screen.board.clear_board()

                if screen.setting_button.check_click(event.pos):  # нажатие кнопки настроек
                    screen.main.start_screen.settings_screen.start()
                if screen.ref_button.check_click(event.pos):  # нажатие кнопки справки
                    screen.main.start_screen.ref_screen.start()

        screen.sc.fill((0, 0, 0))
        screen.render()
        show_stats(screen)
        draw_end_surface(screen, surf)
        screen.render_cursor()
        clock.tick(fps)
        pygame.display.flip()


def draw_end_surface(screen, main_surf):
    '''Отображение информации на экране окончания'''
    global money_now
    one_size = screen.board.cell_size
    lst = []

    surf = pygame.surface.Surface((one_size * 6, one_size * 2))  # создание полотна

    surf.fill('white')
    main_surf.fill('black')

    if is_win:  # инфо при победе
        font = pygame.font.Font(None, round(one_size * 1.4))
        text = font.render('Вы победили!', True, 'white')
    else:  # инфо при поражении
        font = pygame.font.Font(None, round(one_size * 1.3))
        text = font.render('Вас уничтожили!', True, 'white')
    main_surf.blit(text, (one_size // 5, one_size // 5))

    lst.append((f'Заработанные монеты: {money_now}', one_size // 2))
    lst.append((f'Счёт: {screen.score * (20 // screen.steps)}', one_size // 2))

    for i in range(len(lst)):  # отображение инфы
        font = pygame.font.Font(None, lst[i][1])
        text = font.render(lst[i][0], True, 'black')
        surf.blit(text, (10, i * 50 + 20))

    main_surf.blit(surf, (one_size, one_size * 1.5))
    screen.sc.blit(main_surf, (one_size * 8, one_size * 4))


def check_click(screen, mouse_pos):
    '''Проверка на нажатие кнопок'''
    if (screen.button_next_step.rect.left <= mouse_pos[0] <= screen.button_next_step.rect.right
            and screen.button_next_step.rect.top <= mouse_pos[1] <= screen.button_next_step.rect.bottom):
        return 'new_step'  # кнопка след. хода
    if (screen.back_button.rect.left <= mouse_pos[0] <= screen.back_button.rect.right
            and screen.back_button.rect.top <= mouse_pos[1] <= screen.back_button.rect.bottom):
        return 'back_to_menu'  # кнопка назад


def choose_unit(screen, cell_coords):
    '''Функция выбора юнита при нажатии на него (проверка на нажатие)'''
    cell_x, cell_y = cell_coords
    coords = cell_x * screen.board.cell_size + screen.board.left, cell_y * screen.board.cell_size + screen.board.top

    for unit in my_units_group:
        if unit.rect.collidepoint(coords):
            return unit

    return None


def check_borders(board, cell_x, cell_y, dx, dy):
    '''Проверка границ поля'''
    return (dx, dy) != (0, 0) and 0 <= cell_x + dx < len(board.board[0]) and 0 <= cell_y + dy < len(board.board)


def new_step():
    '''Начало новго хода (обновление юнито)'''
    for unit in itertools.chain(my_units_group, enemies_group):
        unit.refresh()


def return_units():
    '''Возвращение юнитов с поля боя в инвентарь при выходе/победе/поражении'''
    dct = {'swordsman': swordsman,
           'archer': archer,
           'cavalry': cavalry,
           'dragon': dragon}
    for unit in my_units_group:
        if unit.name != 'castle':
            dct[unit.name].stock += 1


def render_surfaces(screen, lst_surfaces, color):
    '''Отображение полотен (surfaces) на поле'''
    for surf in lst_surfaces:
        surface, surface_coords = surf
        surface.fill(color)
        surface.set_alpha(60)
        screen.sc.blit(surface, surface_coords)


def can_move(screen):
    '''Проверка на возможность хода юнитом'''
    surfaces_can_move = []
    for un in my_units_group:  # проверка всех юнитов на возможность ходить
        cell = screen.board.get_cell((un.rect.x, un.rect.y))
        lst_steps = select_surfaces(screen.board, un, cell, False)[0]
        if (un.step != 0 and len(lst_steps) and (un.rect.x >= screen.board.left and un.rect.y >= screen.board.top)
                and not action_in_progress and un.name != 'castle'):
            surfaces_can_move.append(
                (pygame.surface.Surface((screen.board.cell_size, screen.board.cell_size)), (un.rect.x, un.rect.y)))
    render_surfaces(screen, surfaces_can_move, 'yellow')

    surfaces_can_move = []
    for un in my_units_group:  # проверка всех юнитов на возможность бить
        cell = screen.board.get_cell((un.rect.x, un.rect.y))
        lst_attack = select_surfaces(screen.board, un, cell, True)[0]
        if (un.do_damage and len(lst_attack) and (un.rect.x >= screen.board.left and un.rect.y >= screen.board.top)
                and not action_in_progress and un.name != 'castle'):
            surfaces_can_move.append(
                (pygame.surface.Surface((screen.board.cell_size, screen.board.cell_size)), (un.rect.x, un.rect.y)))
    render_surfaces(screen, surfaces_can_move, 'orange')


def enemys_move(screen):
    '''Функция обработки ходов юнитов'''
    for unit in enemies_group:
        if unit.step == 0:  # проверка на возможность хода
            continue

        cell = screen.board.get_cell((unit.rect.x, unit.rect.y))
        lst_steps, _ = select_surfaces(screen.board, unit, cell, False)

        if len(lst_steps):  # если есть возможные ходы
            random.shuffle(lst_steps)  # перемешиваем ходы
            choose_cell = random.choice(lst_steps)  # берем рандомный (рандом x2)
            castle_unit_coords = None
            for i in my_units_group:
                if i.name == "castle":  # проверка на башню
                    castle_unit_coords = screen.board.get_cell((i.rect.x, i.rect.y))
                    break
            for step in lst_steps:  # выбор оптимального хода по манхэттеновскому расстоянию
                if abs(step[0] - castle_unit_coords[0]) <= abs(choose_cell[0] - castle_unit_coords[0]):
                    choose_cell = step

            increment_action_in_progress()
            unit.make_step(cell, choose_cell, screen, enemys_attack, [screen, unit, choose_cell])
        else:
            increment_action_in_progress()
            enemys_attack(screen, unit, cell)


def enemys_attack(screen, unit, now_cell):
    '''Функция атаки вражеских юнитов'''
    decrement_action_in_progress()
    lst_steps, _ = select_surfaces(screen.board, unit, now_cell, True)

    if len(lst_steps):  # если есть кого атаковать
        select_attack = random.choice(lst_steps)

        increment_action_in_progress()
        unit.make_attack(select_attack, screen, decrement_action_in_progress, [])


def show_stats(screen):
    '''Отображение статистики клетки/персоанажа при наведении мышкой'''
    stats_surface = pygame.Surface((200, 100))
    font = pygame.font.Font(None, 25)
    stats = []

    for un in itertools.chain(enemies_group, my_units_group, shop_group):  # запись инфы с юнита
        if un.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: {un.title}',  # название
                f'Здоровье: {un.hp}',  # хп
                f'Урон: {un.damage}' + (f' + {un.damage_plus}' if un.attack_type == RANGE_ATTACK else ''),  # урон
                f'Передвижение: {un.step}',  # шаги
                f'Дистанция атаки: {un.distance_attack}'  # дистанция атаки
            ]

    if not len(stats):  # если навели не на юнита (значит на ландшафт)
        for land in landscape_group:  # запись инфы с ландшафта
            if land.rect.collidepoint(pygame.mouse.get_pos()):
                stats = [
                    f'Ландшафт: {land.title}',  # название
                    f'Доп. урон: {land.damage}',  # доп. урон
                    f'Передвижение: {land.move}'  # шаги
                ]

    for i in range(len(stats)):  # отобржение инфы о юните/клетки
        text = font.render(stats[i], True, (255, 255, 255))
        stats_surface.blit(text, (0, i * 20, 100, 100))
    screen.sc.blit(stats_surface, (screen.board.left // 2 - 100, screen.height // 2))  # отображение полотна


def choose_step(screen, unit, cell_coords):
    '''Выбор хода игроком (перемещение - ЛКМ)'''
    lst_steps, lst_surfaces = select_surfaces(screen.board, unit, cell_coords, False)

    if unit.step > 0:  # есть ли ходы
        while True:  # запуск мини-цикла на выбор клетки (для перемещения юнита)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # проверка на выход из игры
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # проверка на нажатие мышкой
                    choose_cell = screen.board.get_cell(event.pos)  # получение координатов выбранной клетки
                    for coords in lst_steps:
                        if coords == choose_cell:  # перемещение юнита в выбранную клетку
                            increment_action_in_progress()
                            unit.make_step(cell_coords, choose_cell, screen, decrement_action_in_progress, [])
                    return

            screen.sc.fill((0, 0, 0))
            screen.render()
            render_surfaces(screen, lst_surfaces, (0, 200, 0))  # TBD Move to main render view
            show_stats(screen)
            screen.render_cursor()
            pygame.display.flip()


def choose_attack(screen, unit, cell_coords):
    '''Выбор хода игроком (перемещение - ПКМ)'''
    lst_steps, lst_surfaces = select_surfaces(screen.board, unit, cell_coords, True)

    if unit.do_damage and len(lst_steps):
        while True:  # запуск мини-цикла на выбор клетки (для атаки юнитом)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # проверка на выход
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # проверка на нажатие мышкой
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


def increment_action_in_progress():
    '''Начало анимции (проверка)'''
    global action_in_progress
    action_in_progress += 1


class BadActionInProgressState(Exception):
    '''Обход ошибки'''
    pass


def decrement_action_in_progress():
    '''Конец анимации (проверка)'''
    global action_in_progress
    action_in_progress -= 1
    if action_in_progress < 0:
        raise BadActionInProgressState()


def select_surfaces(board, unit, cell, is_attack):
    '''Функция выбора и отображения выбранных клетов (подсветка)'''
    lst_surfaces = []
    lst_steps = []
    if not is_attack:  # если перемещние (не атака)
        def add(ran, cell_coords):  # создание рекурсивной функции (умное перемещение)
            cell_x, cell_y = cell_coords

            for dx in (-1, 0, 1):  # обработка в радиусе 1 клетки
                for dy in (-1, 0, 1):
                    minus = 1
                    if abs(dx) != abs(dy):
                        if check_borders(board, cell_x, cell_y, dx, dy):  # проверка на выход за границы
                            if ((board.board[cell_y + dy][cell_x + dx] == 0 and
                                 board.field[cell_y + dy][cell_x + dx] != 1)):  # проверка на занятость поля
                                if board.field[cell_y + dy][cell_x + dx] != 3 or \
                                        board.field[cell_y + dy][cell_x + dx] == 3 and unit.name == 'dragon':
                                    if (cell_x + dx, cell_y + dy) not in lst_steps:
                                        lst_steps.append((cell_x + dx, cell_y + dy))

                                        coords = board.get_cell_coords((cell_x + dx, cell_y + dy))
                                        surface = pygame.surface.Surface((board.cell_size, board.cell_size))
                                        lst_surfaces.append((surface, coords))
                                    if unit.name != 'dragon':  # исключение для дракона на реке
                                        if board.field[cell_y + dy][cell_x + dx] == 2:
                                            minus += 1
                                    if ran - minus > 0:  # запуск рекурсии (для следующего радиуса соседних клеток)
                                        add(ran - minus, (cell_x + dx, cell_y + dy))

        add(unit.step, cell)  # первый запуск функции

    else:  # если атака
        if unit in my_units_group:  # если юниты игрока
            enemies = (2, 3)
        else:  # если юниты врага
            enemies = (1, 4)

        cell_x, cell_y = cell
        for dx in range(-unit.distance_attack, unit.distance_attack + 1):  # проверка по радиусу атаки
            for dy in range(-unit.distance_attack, unit.distance_attack + 1):
                if check_borders(board, cell_x, cell_y, dx, dy):
                    if board.board[cell_y + dy][cell_x + dx] in enemies:
                        lst_steps.append((cell_x + dx, cell_y + dy))

                        coords = board.get_cell_coords((cell_x + dx, cell_y + dy))
                        surface = pygame.surface.Surface((board.cell_size, board.cell_size))
                        lst_surfaces.append((surface, coords))

    return lst_steps, lst_surfaces


def give_damage(screen, select_coords, select_cell, actor):
    '''Нанесение дамага по юниту'''
    global is_win, money_now
    target = 0

    for group in [my_units_group, enemies_group]:
        for unit in group:
            if actor in my_units_group:
                target = 3  # индекс выбранного юнита
            if actor in enemies_group:
                target = 4  # индекс выбранного юнита
            if screen.board.board[select_cell[1]][select_cell[0]] == target and unit.name == "castle":
                unit.recieve_damage(actor)
                if unit.is_dead:
                    for i in range(len(screen.board.board)):
                        for j in range(len(screen.board.board[i])):
                            if screen.board.board[i][j] == target:
                                screen.board.board[i][j] = 0
                    if actor in my_units_group:  # конец игры - победа, запуск финального окна
                        if 3 in screen.progress: # запуск финального экрана всей игры
                            screen.main.go_final_window()
                        else:
                            money_now += 100  # деньги за башню
                            is_win = True  # победа
                            screen.progress.add(int(screen.board.level) + 1)
                            end(screen)
                    if actor in enemies_group:  # конец игры - поражение, запуск финального окна
                        is_win = False  # поражение
                        end(screen)
                    return
            if (unit.rect.x, unit.rect.y) == select_coords:  # проверка клетки
                unit.recieve_damage(actor)
                if unit.is_dead:  # удаление убитого юнита
                    screen.board.board[select_cell[1]][select_cell[0]] = 0

                    if actor in my_units_group:  # получение наград (очков и монет) за убийство
                        dct = {'swordsman': (30, 5),
                               'archer': (35, 25),
                               'cavalry': (45, 20),
                               'dragon': (100, 40)}

                        money, score = dct[unit.name]
                        money_now += money
                        screen.score += score
                return
