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
                cell_coords = screen.board.get_cell(event.pos)
                unit, is_chose_unit = choose_unit(screen, cell_coords)
                if unit != -1 and event.button == 1:
                    choose_step(screen, lst_surfaces, unit, cell_coords, is_chose_unit)
                if unit != -1 and event.button == 3:
                    choose_attack(screen, unit, cell_coords, is_chose_unit)
        screen.sc.fill((0, 0, 0))
        screen.render()
        render(screen, lst_surfaces)
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


def add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy):
    if ((dx, dy) != (0, 0) and
            0 <= cell_x + dx < len(screen.board.board[0]) and
            0 <= cell_y + dy < len(screen.board.board)):
        if screen.board.board[cell_y + dy][cell_x + dx] == 0:
            lst_steps.append((cell_y + dy, cell_x + dx))

            surface_coords_x = x + dx * screen.board.cell_size
            surface_coords_y = y + dy * screen.board.cell_size
            surface_size = screen.board.cell_size, screen.board.cell_size
            surface = pygame.surface.Surface(surface_size)
            lst_surfaces.append(
                (surface, (surface_coords_x, surface_coords_y),
                 (screen.board.cell_size, screen.board.cell_size)))


def choose_step(screen, lst_surfaces, unit, cell_coords, is_chose_unit):
    how_choose_unit = None
    lst_steps = []
    type_unit, coords = unit
    x, y = coords
    cell_x, cell_y = cell_coords
    lst_surfaces.clear()

    if type_unit in swordsman.swordsmans:
        for dx in range(-type_unit.step, type_unit.step + 1):
            for dy in range(-type_unit.step, type_unit.step + 1):
                how_choose_unit = 'swordsman'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy)

    if type_unit in archer.archers:
        for dx in range(-type_unit.step, type_unit.step + 1):
            for dy in range(-type_unit.step, type_unit.step + 1):
                how_choose_unit = 'archer'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy)

    if type_unit in cavalry.cavalrys:
        for dx in range(-type_unit.step, type_unit.step + 1):
            for dy in range(-type_unit.step, type_unit.step + 1):
                how_choose_unit = 'cavalry'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy)

    if type_unit in dragon.dragons:
        for dx in range(-type_unit.step, type_unit.step + 1):
            for dy in range(-type_unit.step, type_unit.step + 1):
                how_choose_unit = 'dragon'
                add_step_surfaces(screen, lst_steps, lst_surfaces, x, y, cell_x, cell_y, dx, dy)

    while is_chose_unit:
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
                            swordsman.Swordsman.update(unit[0], cell_coords, choose_cell, screen)
                            break
                        if how_choose_unit == 'archer':
                            archer.Archer.update(unit[0], cell_coords, choose_cell, screen)
                            break
                        if how_choose_unit == 'cavalry':
                            cavalry.Cavalry.update(unit[0], cell_coords, choose_cell, screen)
                            break
                        if how_choose_unit == 'dragon':
                            dragon.Dragon.update(unit[0], cell_coords, choose_cell, screen)
                            break

                lst_surfaces.clear()
                is_chose_unit = False

        screen.sc.fill((0, 0, 0))
        screen.render()
        render(screen, lst_surfaces)
        pygame.display.flip()


def choose_attack(screen, unit, cell_coords, is_chose_unit):
    pass  # атака на вражеского юнита
    

def render(screen, lst_surfaces):
    for surf in lst_surfaces:
        surface, surface_coords, surface_size = surf

        pygame.draw.rect(surface, (0, 200, 0, 0.6), (0, 0, *surface_size))
        screen.sc.blit(surface, surface_coords)
