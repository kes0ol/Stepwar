import random
import sys

import pygame

import swordsman, archer, cavalry, dragon, castle
import enemys
import landscapes

is_win = None


def start(screen):
    global is_win
    enemys_move(screen)

    fps = 120
    clock = pygame.time.Clock()
    running = True
    while screen.gameplay and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    new_step()
                    screen.board.clear_board(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                select_button = check_click(screen, event.pos)
                if select_button == 'new_step':
                    screen.steps += 1
                    new_step()
                    enemys_move(screen)
                if select_button == 'back_to_menu':
                    running = False
                    new_step()
                    screen.board.clear_board(screen)
                if screen.setting_button.check_click(event.pos):
                    screen.main.start_screen.settings_screen.start()
                if screen.ref_button.check_click(event.pos):
                    screen.main.start_screen.ref_screen.start()

                cell_coords = screen.board.get_cell(event.pos)
                unit, is_choose_unit = choose_unit(screen, cell_coords)
                if unit != -1 and event.button == 1:
                    is_attack = False
                    choose_step(screen, unit, cell_coords, is_choose_unit, select_button, is_attack)
                if unit != -1 and event.button == 3:
                    is_attack = True
                    choose_attack(screen, unit, cell_coords, is_choose_unit, is_attack)

        screen.sc.fill((0, 0, 0))
        screen.render()
        screen.render_cursor()
        show_stats(screen)
        clock.tick(fps)
        pygame.display.flip()


def end(screen):
    surf = pygame.Surface((8 * screen.board.cell_size, 5 * screen.board.cell_size))

    fps = 120
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    swordsman.stock = len(swordsman.swordsmans) - 1
                    archer.stock = len(archer.archers) - 1
                    cavalry.stock = len(cavalry.cavalrys) - 1
                    dragon.stock = len(dragon.dragons) - 1

                    running = False
                    screen.gameplay = False

                    new_step()
                    screen.board.clear_board(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                select_button = check_click(screen, event.pos)

                if select_button == 'back_to_menu':
                    running = False
                    screen.gameplay = False

                    new_step()
                    screen.board.clear_board(screen)

        screen.sc.fill((0, 0, 0))
        screen.render()
        show_stats(screen)
        draw_end_surface(screen, surf)
        screen.render_cursor()
        clock.tick(fps)
        pygame.display.flip()


def draw_end_surface(screen, main_surf):
    win_sound = pygame.mixer.Sound('music/win.wav')
    lose_sound = pygame.mixer.Sound('music/lose.wav')

    surf = pygame.surface.Surface((400, 100))
    lst = []

    if is_win:
        win_sound.play()
        lst.append(('Вы победили!', 100))
    else:
        lose_sound.play()
        lst.append(('Вас уничтожили!', 90))

    lst.append((f'Заработанные монеты: {screen.money}', 30))
    lst.append((f'Счёт: {screen.score * (20 // screen.steps)}', 30))

    surf.fill('white')
    main_surf.fill('black')

    font = pygame.font.Font(None, lst[0][1])
    text = font.render(lst[0][0], True, 'white')
    main_surf.blit(text, (100, 100))

    for i in range(len(lst[1:])):
        font = pygame.font.Font(None, lst[1:][i][1])
        text = font.render(lst[1:][i][0], True, 'black')
        surf.blit(text, (10, i * 50 + 20))

    main_surf.blit(surf, (50, 100))
    screen.sc.blit(main_surf, (500, 250))


def check_borders(screen, cell_x, cell_y, dx, dy):
    if ((dx, dy) != (0, 0) and
            0 <= cell_x + dx < len(screen.board.board[0]) and
            0 <= cell_y + dy < len(screen.board.board)):
        return True
    return False


def enemys_move(screen):
    for group in [enemys.swordsmans, enemys.archers, enemys.cavalrys, enemys.dragons]:
        for unit in group:
            lst_steps = []
            r = unit.step
            cell_x, cell_y = screen.board.get_cell((unit.rect.x, unit.rect.y))

            def add(ran, cell_coords):
                cell_x, cell_y = cell_coords

                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        minus = 1
                        if abs(dx) != (abs(dy)):
                            if check_borders(screen, cell_x, cell_y, dx, dy):
                                if ((screen.board.board[cell_y + dy][cell_x + dx] == 0 and
                                     screen.board.field[cell_y + dy][cell_x + dx] != 1)):
                                    if screen.board.field[cell_y + dy][cell_x + dx] != 3 or \
                                            screen.board.field[cell_y + dy][cell_x + dx] == 3 and unit.name == 'dragon':
                                        for i in lst_steps:
                                            if i == (cell_y + dy, cell_x + dx):
                                                break
                                        else:
                                            if dx < 0:
                                                lst_steps.append((cell_y + dy, cell_x + dx))
                                            lst_steps.append((cell_y + dy, cell_x + dx))
                                    else:
                                        minus = ran

                                    if screen.board.field[cell_y][cell_x] == 2:
                                        minus = 2

                                    if ran - minus > 0:
                                        add(ran - minus, (cell_x + dx, cell_y + dy))

            add(r, (cell_x, cell_y))

            if len(lst_steps) > 0:
                choise_cell = random.choice(lst_steps)
                select_coords = (choise_cell[1] * screen.board.cell_size + screen.board.left,
                                 choise_cell[0] * screen.board.cell_size + screen.board.top)

                if screen.board.board[choise_cell[0]][choise_cell[1]] == 0 and (cell_x, cell_y) != (-1, -1):
                    screen.board.board[cell_y][cell_x] = 0
                    screen.board.board[choise_cell[0]][choise_cell[1]] = 2
                    unit.rect.x, unit.rect.y = select_coords

            enemys_attack(screen, unit, (cell_x, cell_y))


def enemys_attack(screen, unit, now_cell):
    click_sound = pygame.mixer.Sound('music/kill_hit.wav')
    global is_win

    can_attack = []
    for dx in range(-unit.distance_attack, unit.distance_attack + 1):
        for dy in range(-unit.distance_attack, unit.distance_attack + 1):
            n_x, n_y = now_cell[0] + dx, now_cell[1] + dy

            if (0 <= n_x <= screen.board.width - unit.distance_attack and
                    0 <= n_y <= screen.board.height - unit.distance_attack):
                if screen.board.board[n_y][n_x] in [1, 4]:
                    can_attack.append((n_x, n_y))

    if len(can_attack) > 0:
        select_attack = random.choice(can_attack)
        damage_castle = True

        for group in [swordsman.swordsmans, archer.archers, cavalry.cavalrys, dragon.dragons, castle.castles]:
            for un in group:
                if screen.board.board[select_attack[1]][select_attack[0]] == 4 and damage_castle:
                    for cas in castle.castles:
                        cas.hp -= unit.damage

                        if cas.hp <= 0:
                            cas.kill()
                            screen.board.board[select_attack[1]][select_attack[0]] = 0

                            for i in range(len(screen.board.board)):
                                for j in range(len(screen.board.board[i])):
                                    if screen.board.board[i][j] == 4:
                                        screen.board.board[i][j] = 0
                            is_win = False
                            end(screen)

                        damage_castle = False
                        break
                    break

                elif ((select_attack[0] * screen.board.cell_size + screen.board.left,
                       select_attack[1] * screen.board.cell_size + screen.board.top) == (un.rect.x, un.rect.y)):
                    un.hp -= unit.damage
                    if un.hp <= 0:
                        click_sound.play()
                        un.kill()
                        screen.board.board[select_attack[1]][select_attack[0]] = 0
                    break


def show_stats(screen):
    stats_surface = pygame.Surface((200, 100))
    font = pygame.font.Font(None, 25)
    stats = []

    for group in [swordsman.swordsmans, archer.archers, cavalry.cavalrys, dragon.dragons, castle.castles,
                  enemys.swordsmans, enemys.archers, enemys.cavalrys, enemys.dragons, enemys.castles]:
        for un in group:
            if un.rect.collidepoint(pygame.mouse.get_pos()):
                stats = [
                    f'Тип юнита: {un.title}',
                    f'Здоровье: {un.hp}',
                    f'Урон: {un.damage}',
                    f'Передвижение: {un.step}',
                    f'Дистанция атаки: {un.distance_attack}'
                ]
                if group in [swordsman.swordsmans, archer.archers, cavalry.cavalrys, dragon.dragons]:
                    stats[2] = f'Урон: {un.damage} + {un.damage_plus}'

    if len(stats) == 0:
        for land in landscapes.landscapes:
            if land.rect.collidepoint(pygame.mouse.get_pos()):
                stats = [
                    f'Ландшафт: {land.title}',
                    f'Доп. урон: {land.damage}',
                    f'Передвижение: {land.move}'
                ]

    for i in range(len(stats)):
        text = font.render(stats[i], True, (255, 255, 255))
        stats_surface.blit(text, (0, i * 20, 100, 100))
    screen.sc.blit(stats_surface, (screen.board.left // 2 - 100, 600))


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

    for sword in swordsman.swordsmans:
        if (sword.rect.x, sword.rect.y) == coords:
            unit = sword
            return unit, True
    for arc in archer.archers:
        if (arc.rect.x, arc.rect.y) == coords:
            unit = arc
            return unit, True
    for cav in cavalry.cavalrys:
        if (cav.rect.x, cav.rect.y) == coords:
            unit = cav
            return unit, True
    for drg in dragon.dragons:
        if (drg.rect.x, drg.rect.y) == coords:
            unit = drg
            return unit, True

    return -1, -1


def add_step_surfaces(screen, unit, lst_steps, lst_surfaces, cell_x, cell_y, unit_range, is_attack):
    if not is_attack:
        r = unit_range

        def add(ran, cell_coords):
            cell_x, cell_y = cell_coords

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    minus = 1
                    if abs(dx) != abs(dy):
                        if check_borders(screen, cell_x, cell_y, dx, dy):
                            if ((screen.board.board[cell_y + dy][cell_x + dx] == 0 and
                                 screen.board.field[cell_y + dy][cell_x + dx] != 1)):
                                if screen.board.field[cell_y + dy][cell_x + dx] != 3 or \
                                        screen.board.field[cell_y + dy][cell_x + dx] == 3 and unit.name == 'dragon':
                                    for i in lst_steps:
                                        if i == (cell_y + dy, cell_x + dx):
                                            break
                                    else:
                                        lst_steps.append((cell_y + dy, cell_x + dx))

                                        surface_coords_x = (cell_x + dx) * screen.board.cell_size + screen.board.left
                                        surface_coords_y = (cell_y + dy) * screen.board.cell_size + screen.board.top
                                        surface = pygame.surface.Surface(
                                            (screen.board.cell_size, screen.board.cell_size))
                                        lst_surfaces.append(
                                            (surface, (surface_coords_x, surface_coords_y),
                                             (screen.board.cell_size, screen.board.cell_size)))
                                else:
                                    minus = ran

                                if screen.board.field[cell_y][cell_x] == 2:
                                    minus = 2

                                if ran - minus > 0:
                                    add(ran - minus, (cell_x + dx, cell_y + dy))

        add(r, (cell_x, cell_y))

    else:
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                if check_borders(screen, cell_x, cell_y, dx, dy):
                    if screen.board.board[cell_y + dy][cell_x + dx] in [2, 3]:
                        lst_steps.append((cell_y + dy, cell_x + dx))

                        surface_coords_x = (cell_x + dx) * screen.board.cell_size + screen.board.left
                        surface_coords_y = (cell_y + dy) * screen.board.cell_size + screen.board.top
                        surface = pygame.surface.Surface((screen.board.cell_size, screen.board.cell_size))
                        lst_surfaces.append(
                            (surface, (surface_coords_x, surface_coords_y),
                             (screen.board.cell_size, screen.board.cell_size)))


def select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack):
    lst_steps = []
    cell_x, cell_y = cell_coords
    lst_surfaces.clear()

    if not is_attack:
        unit_range = unit.step
    else:
        unit_range = unit.distance_attack

    groups = [swordsman.swordsmans, archer.archers, cavalry.cavalrys, dragon.dragons]

    for id in range(len(groups)):
        if unit in groups[id]:
            how_choose_unit = unit.name
            add_step_surfaces(screen, unit, lst_steps, lst_surfaces, cell_x, cell_y, unit_range, is_attack)
            return unit, lst_steps, how_choose_unit


def choose_step(screen, unit, cell_coords, is_choose_unit, select_button, is_attack):
    lst_surfaces = []
    type_unit, lst_steps, how_choose_unit = select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack)
    if type_unit.step > 0:
        while is_choose_unit and select_button != 'new_step':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    select_button = check_click(screen, event.pos)
                    choose_cell = tuple(reversed(list(screen.board.get_cell(event.pos))))
                    for coords in lst_steps:
                        if coords == choose_cell:
                            if how_choose_unit == 'swordsman':
                                type_unit.step = 0
                                swordsman.Swordsman.update(unit, cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'archer':
                                type_unit.step = 0
                                archer.Archer.update(unit, cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'cavalry':
                                type_unit.step = 0
                                cavalry.Cavalry.update(unit, cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'dragon':
                                type_unit.step = 0
                                dragon.Dragon.update(unit, cell_coords, choose_cell, screen, is_attack)

                    lst_surfaces.clear()
                    is_choose_unit = False

            screen.sc.fill((0, 0, 0))
            screen.render()
            render(screen, lst_surfaces, (0, 200, 0))
            show_stats(screen)
            screen.render_cursor()
            pygame.display.flip()


def choose_attack(screen, unit, cell_coords, is_chose_unit, is_attack):
    lst_surfaces = []
    type_unit, lst_steps, how_choose_unit = select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack)
    if type_unit.do_damage:
        while is_chose_unit and is_attack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choose_cell = tuple(reversed(list(screen.board.get_cell(event.pos))))
                    for coords in lst_steps:
                        if coords == choose_cell:
                            if how_choose_unit == 'swordsman':
                                swordsman.Swordsman.update(unit, cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'archer':
                                archer.Archer.update(unit, cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'cavalry':
                                cavalry.Cavalry.update(unit, cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'dragon':
                                dragon.Dragon.update(unit, cell_coords, choose_cell, screen, is_attack)
                            type_unit.do_damage = False
                    lst_surfaces.clear()
                    is_attack = False

            screen.sc.fill((0, 0, 0))
            screen.render()
            render(screen, lst_surfaces, (200, 0, 0))
            show_stats(screen)
            screen.render_cursor()
            pygame.display.flip()


def give_damage(screen, select_coords, select_cell, damage_team_unit):
    kill_sound = pygame.mixer.Sound('music/kill_hit.wav')
    global is_win
    damage_at_enemy_castle = True

    for group in [enemys.swordsmans, enemys.archers, enemys.cavalrys, enemys.dragons, enemys.castles]:
        for unit in group:
            if screen.board.board[select_cell[1]][select_cell[0]] == 3 and damage_at_enemy_castle:  # проверка башни
                for enemy_castle in enemys.castles:
                    enemy_castle.hp -= damage_team_unit
                    if enemy_castle.hp <= 0:
                        enemy_castle.kill()
                        screen.board.board[select_cell[1]][select_cell[0]] = 0
                        for i in range(len(screen.board.board)):
                            for j in range(len(screen.board.board[i])):
                                if screen.board.board[i][j] == 3:
                                    screen.board.board[i][j] = 0
                        screen.money += 100
                        is_win = True
                        end(screen)

                    damage_at_enemy_castle = False
                    break
                break

            if (unit.rect.x, unit.rect.y) == select_coords:
                unit.hp -= damage_team_unit
                if unit.hp <= 0:
                    kill_sound.play()
                    unit.kill()
                    screen.board.board[select_cell[1]][select_cell[0]] = 0

                    if unit.name == 'swordsman':
                        screen.money += 10
                        screen.score += 5
                    if unit.name == 'archer':
                        screen.money += 15
                        screen.score += 25
                    if unit.name == 'cavalry':
                        screen.money += 20
                        screen.score += 20
                    if unit.name == 'dragon':
                        screen.money += 50
                        screen.score += 40
                break


def new_step():
    for sword in swordsman.swordsmans:
        sword.step = 2
        sword.do_damage = True
    for arc in archer.archers:
        arc.step = 1
        arc.do_damage = True
    for cav in cavalry.cavalrys:
        cav.step = 3
        cav.do_damage = True
    for drg in dragon.dragons:
        drg.step = 4
        drg.do_damage = True


def render(screen, lst_surfaces, color):
    for surf in lst_surfaces:
        surface, surface_coords, surface_size = surf
        surface.fill(color)
        surface.set_alpha(80)
        screen.sc.blit(surface, surface_coords)
