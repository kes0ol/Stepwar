import sys
import random
import pygame

import enemys
import swordsman
import archer
import cavalry
import dragon
import castle


def start(screen):
    lst_surfaces = []
    enemys_move(screen)

    while screen.gameplay:
        fps = 120
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.board.gameplay = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                select_button = check_click(screen, event.pos)
                if select_button == 'new_step':
                    new_step()
                    enemys_move(screen)
                if select_button == 'back_to_menu':
                    screen.gameplay = False

                    new_step()
                    screen.board.clear_board(screen)

                cell_coords = screen.board.get_cell(event.pos)
                unit, is_choose_unit = choose_unit(screen, cell_coords)
                if unit != -1 and event.button == 1:
                    is_attack = False
                    choose_step(screen, lst_surfaces, unit, cell_coords, is_choose_unit, select_button, is_attack)
                if unit != -1 and event.button == 3:
                    is_attack = True
                    choose_attack(screen, lst_surfaces, unit, cell_coords, is_choose_unit, is_attack)

        screen.sc.fill((0, 0, 0))
        screen.render()
        show_stats(screen)
        clock.tick(fps)
        pygame.display.flip()


def enemys_move(screen):
    width, height = screen.board.width * screen.board.cell_size, screen.board.height * screen.board.cell_size
    moves = [(-screen.board.cell_size, 0), (-screen.board.cell_size, 0),
             (-screen.board.cell_size, -screen.board.cell_size),
             (0, -screen.board.cell_size), (screen.board.cell_size, -screen.board.cell_size),
             (screen.board.cell_size, 0), (screen.board.cell_size, screen.board.cell_size), (0, screen.board.cell_size),
             (-screen.board.cell_size, screen.board.cell_size)]
    for group in [enemys.swordsmans, enemys.archers, enemys.cavalrys, enemys.dragons]:
        for unit in group:
            now_cell = screen.board.get_cell((unit.rect.x, unit.rect.y))

            choise_move = random.choice(moves)
            distance_move = random.randint(1, unit.step)
            select_coords = (unit.rect.x + choise_move[0] * distance_move,
                             unit.rect.y + choise_move[1] * distance_move)
            select_cell = screen.board.get_cell(select_coords)

            if (screen.board.left <= select_coords[0] <= width and screen.board.top <= select_coords[1] <= height and
                    not screen.board.board[select_cell[1]][select_cell[0]] and
                    not screen.board.field[select_cell[1]][select_cell[0]] and select_cell != (-1, -1)):
                screen.board.board[now_cell[1]][now_cell[0]] = 0
                screen.board.board[select_cell[1]][select_cell[0]] = 2
                unit.rect.x, unit.rect.y = select_coords

            enemys_attack(screen, unit, now_cell)


def enemys_attack(screen, unit, now_cell):
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
                        damage_castle = False
                        break
                    break

                elif ((select_attack[0] * screen.board.cell_size + screen.board.left,
                       select_attack[1] * screen.board.cell_size + screen.board.top) == (un.rect.x, un.rect.y)):
                    un.hp -= unit.damage
                    if un.hp <= 0:
                        un.kill()
                        screen.board.board[select_attack[1]][select_attack[0]] = 0
                    break


def show_stats(screen):
    stats_surface = pygame.Surface((200, 100))
    font = pygame.font.Font(None, 25)
    stats = []

    for sword in swordsman.swordsmans:
        if sword.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: Рыцарь',
                f'Здоровье: {sword.hp}',
                f'Урон: {sword.damage}',
                f'Передвижение: {sword.step}',
                f'Дистанция атаки: {sword.distance_attack}'
            ]
    for arc in archer.archers:
        if arc.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: Лучник',
                f'Здоровье: {arc.hp}',
                f'Урон: {arc.damage}',
                f'Передвижение: {arc.step}',
                f'Дистанция атаки: {arc.distance_attack}'
            ]
    for cav in cavalry.cavalrys:
        if cav.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: Кавалерия',
                f'Здоровье: {cav.hp}',
                f'Урон: {cav.damage}',
                f'Передвижение: {cav.step}',
                f'Дистанция атаки: {cav.distance_attack}'
            ]
    for drg in dragon.dragons:
        if drg.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: Дракон',
                f'Здоровье: {drg.hp}',
                f'Урон: {drg.damage}',
                f'Передвижение: {drg.step}',
                f'Дистанция атаки: {drg.distance_attack}'
            ]

    for cas in castle.castles:
        if cas.rect.collidepoint(pygame.mouse.get_pos()):
            stats = [
                f'Тип юнита: Замок',
                f'Здоровье: {cas.hp}',
                f'Урон: {cas.damage}',
                f'Передвижение: {cas.step}',
                f'Дистанция атаки: {cas.distance_attack}'
            ]

    for group in [enemys.swordsmans, enemys.archers, enemys.cavalrys, enemys.dragons, enemys.castles]:
        for unit in group:
            if unit.rect.collidepoint(pygame.mouse.get_pos()):
                stats = [
                    f'Тип юнита: {unit.name}',
                    f'Здоровье: {unit.hp}',
                    f'Урон: {unit.damage}',
                    f'Передвижение: {unit.step}',
                    f'Дистанция атаки: {unit.distance_attack}']

    for i in range(len(stats)):
        text = font.render(stats[i], True, (255, 255, 255))
        stats_surface.blit(text, (0, i * 20, 100, 100))
    screen.sc.blit(stats_surface, (screen.board.left // 2 - 100, 500))


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
    def check_borders(cell_x, cell_y, dx, dy):
        if ((dx, dy) != (0, 0) and
                0 <= cell_x + dx < len(screen.board.board[0]) and
                0 <= cell_y + dy < len(screen.board.board)):
            return True
        return False

    if not is_attack:
        r = unit_range

        def add(ran, cell_coords):
            cell_x, cell_y = cell_coords

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if check_borders(cell_x, cell_y, dx, dy):
                        if ((screen.board.board[cell_y + dy][cell_x + dx] == 0 and
                             screen.board.field[cell_y + dy][cell_x + dx] != 1)):
                            for i in lst_steps:
                                if i == (cell_y + dy, cell_x + dx):
                                    break
                            else:
                                lst_steps.append((cell_y + dy, cell_x + dx))

                                surface_coords_x = (cell_x + dx) * screen.board.cell_size + screen.board.left
                                surface_coords_y = (cell_y + dy) * screen.board.cell_size + screen.board.top
                                surface = pygame.surface.Surface((screen.board.cell_size, screen.board.cell_size))
                                lst_surfaces.append(
                                    (surface, (surface_coords_x, surface_coords_y),
                                     (screen.board.cell_size, screen.board.cell_size)))

                            minus = 1

                            if screen.board.field[cell_y][cell_x] == 2:
                                minus = 2

                            if screen.board.field[cell_y][cell_x] == 3:
                                if unit.name != 'dragon':
                                    pass

                            if ran - minus > 0:
                                add(ran - minus, (cell_x + dx, cell_y + dy))

        add(r, (cell_x, cell_y))

    else:
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                if check_borders(cell_x, cell_y, dx, dy):
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


def choose_step(screen, lst_surfaces, unit, cell_coords, is_choose_unit, select_button, is_attack):
    type_unit, lst_steps, how_choose_unit = select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack)
    if type_unit.step > 0:
        while is_choose_unit and select_button != 'new_step':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen.gameplay = False
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
            pygame.display.flip()


def choose_attack(screen, lst_surfaces, unit, cell_coords, is_chose_unit, is_attack):
    type_unit, lst_steps, how_choose_unit = select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack)
    if type_unit.do_damage:
        while is_chose_unit and is_attack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen.gameplay = False
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
            pygame.display.flip()


def give_damage(screen, select_coords, select_cell, damage_team_unit):
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
                    damage_at_enemy_castle = False
                    break
                break

            if (unit.rect.x, unit.rect.y) == select_coords:
                unit.hp -= damage_team_unit
                if unit.hp <= 0:
                    unit.kill()
                    screen.board.board[select_cell[1]][select_cell[0]] = 0
                break


def new_step():
    for sword in swordsman.swordsmans:
        sword.step = 1
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
