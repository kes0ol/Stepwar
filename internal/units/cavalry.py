import os

import pygame

from internal.different.animation import AnimationParams
from internal.different.global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, \
    ANIMATION_MOVE, ANIMATION_END_MOVE, ANIMATION_DEATH, MELEE_ATTACK, QUANTITY_CAVALRY
from internal.units.unit import Unit


class Cavalry(Unit):
    '''Создание класса кавалерии'''

    def __init__(self, x, y, image_size, group, death_callback, mirror_animation=False):
        '''Инициализация класса'''
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'cavalry.jpg'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 9, 1, 130, 130, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 9, 1, 130, 130, 0, 130, 8),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 130, 130, 0, 0, 8),
            ANIMATION_MOVE: AnimationParams(sheet, 7, 1, 130, 130, 0, 0, 4),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 130, 130, 0, 0, 1),
            ANIMATION_DEATH: AnimationParams(sheet, 8, 1, 130, 130, 0, 390, 8)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, ['music', 'cavalry_hit.wav'],
                         death_callback, mirror_animation)  # анимации кавалерии
        self.init_stats(5, 1, MELEE_ATTACK, 80, 30, 'cavalry', 'Кавалерия', QUANTITY_CAVALRY)


def set_view_stock(screen, coords, size):  # отображение количества лучников
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
