import sys

import pygame

import swordsman
import archer
import cavalry
import dragon


def start(screen):
    lst_surfaces = []
    while screen.board.gameplay:
        fps = 120
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.board.gameplay = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_new_step = check_click(screen, event.pos)
                if is_new_step:
                    new_step(screen)
                cell_coords = screen.board.get_cell(event.pos)
                unit, is_choose_unit = choose_unit(screen, cell_coords)
                if unit != -1 and event.button == 1:
                    is_attack = False
                    choose_step(screen, lst_surfaces, unit, cell_coords, is_choose_unit, is_new_step, is_attack)
                if unit != -1 and event.button == 3:
                    is_attack = True
                    choose_attack(screen, lst_surfaces, unit, cell_coords, is_choose_unit, is_attack)
        screen.sc.fill((0, 0, 0))
        screen.render()
        clock.tick(fps)
        pygame.display.flip()


def choose_unit(screen, cell_coords):
    cell_x, cell_y = cell_coords
    coords = cell_x * screen.board.cell_size + screen.board.left, cell_y * screen.board.cell_size + screen.board.top

    for sword in swordsman.swordsmans:
        if (sword.rect.x, sword.rect.y) == coords:
            unit = sword, coords
            return unit, True
    for arc in archer.archers:
        if (arc.rect.x, arc.rect.y) == coords:
            unit = arc, coords
            return unit, True
    for cav in cavalry.cavalrys:
        if (cav.rect.x, cav.rect.y) == coords:
            unit = cav, coords
            return unit, True
    for drg in dragon.dragons:
        if (drg.rect.x, drg.rect.y) == coords:
            unit = drg, coords
            return unit, True

    return -1, -1


def add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy, is_attack):
    if ((dx, dy) != (0, 0) and
            0 <= cell_x + dx < len(screen.board.board[0]) and
            0 <= cell_y + dy < len(screen.board.board)):
        if (screen.board.board[cell_y + dy][cell_x + dx] == 0 and not is_attack or
                screen.board.board[cell_y + dy][cell_x + dx] == 2 and is_attack):
            lst_steps.append((cell_y + dy, cell_x + dx))

            surface_coords_x = x + dx * screen.board.cell_size
            surface_coords_y = y + dy * screen.board.cell_size
            surface_size = screen.board.cell_size, screen.board.cell_size
            surface = pygame.surface.Surface(surface_size)
            lst_surfaces.append(
                (surface, (surface_coords_x, surface_coords_y),
                 (screen.board.cell_size, screen.board.cell_size)))


def select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack):
    how_choose_unit = None
    lst_steps = []
    type_unit, coords = unit
    x, y = coords
    cell_x, cell_y = cell_coords
    lst_surfaces.clear()

    if not is_attack:
        unit_range = type_unit.step
    else:
        unit_range = type_unit.distance_attack
    if type_unit in swordsman.swordsmans:
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                how_choose_unit = 'swordsman'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy, is_attack)
        return type_unit, lst_steps, how_choose_unit

    if type_unit in archer.archers:
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                how_choose_unit = 'archer'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy, is_attack)
        return type_unit, lst_steps, how_choose_unit

    if type_unit in cavalry.cavalrys:
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                how_choose_unit = 'cavalry'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy, is_attack)
        return type_unit, lst_steps, how_choose_unit

    if type_unit in dragon.dragons:
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                how_choose_unit = 'dragon'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy, is_attack)
        return type_unit, lst_steps, how_choose_unit


def choose_step(screen, lst_surfaces, unit, cell_coords, is_chose_unit, is_new_step, is_attack):
    type_unit, lst_steps, how_choose_unit = select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack)
    if type_unit.step > 0:
        while is_chose_unit and not is_new_step:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen.board.gameplay = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_new_step = check_click(screen, event.pos)
                    choose_cell = tuple(reversed(list(screen.board.get_cell(event.pos))))
                    for coords in lst_steps:
                        if coords == choose_cell:
                            move = abs(cell_coords[0] - choose_cell[1]) + abs(cell_coords[1] - choose_cell[0])
                            if how_choose_unit == 'swordsman':
                                if abs(cell_coords[0] - choose_cell[1]) != abs(
                                        cell_coords[1] - cell_coords[0]):  # неверно
                                    move //= 2 - 1
                                type_unit.step -= move
                                swordsman.Swordsman.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'archer':
                                if abs(cell_coords[0] - choose_cell[1]) != abs(
                                        cell_coords[1] - cell_coords[0]):  # неверно
                                    move //= 2 - 1
                                type_unit.step -= move
                                archer.Archer.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'cavalry':
                                if abs(cell_coords[0] - choose_cell[1]) != abs(
                                        cell_coords[1] - cell_coords[0]):  # неверно
                                    move //= 2 - 1
                                type_unit.step -= move
                                cavalry.Cavalry.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'dragon':
                                if abs(cell_coords[0] - choose_cell[1]) != abs(
                                        cell_coords[1] - cell_coords[0]):  # неверно
                                    move //= 2 - 1
                                type_unit.step -= move
                                dragon.Dragon.update(unit[0], cell_coords, choose_cell, screen, is_attack)

                    lst_surfaces.clear()
                    is_chose_unit = False

            screen.sc.fill((0, 0, 0))
            screen.render()
            render(screen, lst_surfaces, (0, 200, 0))
            pygame.display.flip()


def choose_attack(screen, lst_surfaces, unit, cell_coords, is_chose_unit, is_attack):
    type_unit, lst_steps, how_choose_unit = select_surfaces(screen, unit, cell_coords, lst_surfaces, is_attack)
    if type_unit.do_damage:
        while is_chose_unit and is_attack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen.board.gameplay = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choose_cell = tuple(reversed(list(screen.board.get_cell(event.pos))))
                    for coords in lst_steps:
                        if coords == choose_cell:
                            if how_choose_unit == 'swordsman':
                                swordsman.Swordsman.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'archer':
                                archer.Archer.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'cavalry':
                                cavalry.Cavalry.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            if how_choose_unit == 'dragon':
                                dragon.Dragon.update(unit[0], cell_coords, choose_cell, screen, is_attack)
                            type_unit.do_damage = False
                    lst_surfaces.clear()
                    is_chose_unit = False

            screen.sc.fill((0, 0, 0))
            screen.render()
            render(screen, lst_surfaces, (200, 0, 0))
            pygame.display.flip()


def check_click(screen, mouse_pos):
    if (screen.button_next_step.button_rect.left <= mouse_pos[0] <= screen.button_next_step.button_rect.right
            and screen.button_next_step.button_rect.top <= mouse_pos[1] <= screen.button_next_step.button_rect.bottom):
        return True
    return False


def new_step(screen):
    for sword in swordsman.swordsmans:
        sword.step = 1
    for arc in archer.archers:
        arc.step = 1
    for cav in cavalry.cavalrys:
        cav.step = 3
    for drg in dragon.dragons:
        drg.step = 4
    screen.board.new_step = False


def render(screen, lst_surfaces, color):
    for surf in lst_surfaces:
        surface, surface_coords, surface_size = surf

        pygame.draw.rect(surface, color, (0, 0, *surface_size))
        screen.sc.blit(surface, surface_coords)
