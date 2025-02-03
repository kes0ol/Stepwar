import os

import pygame

from development.different.animation import AnimationParams
from development.different.global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, \
    ANIMATION_MOVE, ANIMATION_END_MOVE, ANIMATION_DEATH, MELEE_ATTACK
from development.units.unit import Unit


class Cavalry(Unit):
    def __init__(self, x, y, image_size, group, damage_func=True, mirror_animation=False):
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'cavalry.png'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 9, 1, 130, 130, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 9, 1, 130, 130, 0, 130, 8),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 130, 130, 0, 0, 8),
            ANIMATION_MOVE: AnimationParams(sheet, 7, 1, 130, 130, 0, 0, 8),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 130, 130, 0, 0, 1),
            ANIMATION_DEATH: AnimationParams(sheet, 8, 1, 130, 130, 0, 390, 8)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, damage_func, mirror_animation)
        self.init_stats(4, 1, MELEE_ATTACK, 120, 40, 'cavalry', 'Кавалерия', 0)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
