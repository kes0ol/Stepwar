import pygame

import mapping
import swordsman
import cavalry


def start(screen):
    lst_surfaces = []
    while screen.board.gameplay:
        fps = 120
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.board.gameplay = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell_coords = screen.board.get_cell(event.pos)
                unit = choose_unit(screen, cell_coords)
                if unit != -1:
                    choose_step(screen, lst_surfaces, unit, cell_coords)
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
            return unit
    for cav in cavalry.cavalrys:
        if (cav.rect.x, cav.rect.y) == coords:
            unit = cav, coords
            return unit
    return -1


def choose_step(screen, lst_surfaces, unit, cell_coords):
    type_unit, coords = unit
    x, y = coords
    cell_x, cell_y = cell_coords
    lst_surfaces.clear()
    if type_unit in swordsman.swordsmans:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (dx, dy) != (0, 0) and screen.board.board[cell_y + dy][cell_x + dx] == 0:
                    surface_coords_x = x + dx * screen.board.cell_size
                    surface_coords_y = y + dy * screen.board.cell_size
                    surface_size = screen.board.cell_size, screen.board.cell_size
                    surface = pygame.surface.Surface(surface_size)
                    lst_surfaces.append(
                        (surface, (surface_coords_x, surface_coords_y),
                         (screen.board.cell_size, screen.board.cell_size)))

    if type_unit in cavalry.cavalrys:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if (dx, dy) != (0, 0) and screen.board.board[cell_y + dy][cell_x + dx] == 0:
                    surface_coords_x = x + dx * screen.board.cell_size
                    surface_coords_y = y + dy * screen.board.cell_size
                    surface_size = screen.board.cell_size, screen.board.cell_size
                    surface = pygame.surface.Surface(surface_size)
                    lst_surfaces.append(
                        (surface, (surface_coords_x, surface_coords_y),
                         (screen.board.cell_size, screen.board.cell_size)))


def render(screen, lst_surfaces):
    for surf in lst_surfaces:
        surface, surface_coords, surface_size = surf

        pygame.draw.rect(surface, (0, 200, 0, 0.6), (0, 0, *surface_size))
        screen.sc.blit(surface, surface_coords)
