import os

import pygame

from internal.different.animation import AnimationParams
from internal.different.global_vars import ANIMATION_ATTACK, ANIMATION_IDLE, ANIMATION_MOVE, \
    ANIMATION_BEGIN_MOVE, ANIMATION_END_MOVE, ANIMATION_DEATH, MELEE_ATTACK, UNIT_DRAGON, QUANTITY_DRAGON
from internal.units.unit import Unit


class Dragon(Unit):
    '''Создание класса дракона'''

    def __init__(self, x, y, image_size, group, death_callback, mirror_animation=False):
        '''Инициализация класса'''
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'dragon.png'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 4, 1, 125, 125, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 7, 1, 170, 170, 0, 170, 8),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 3, 1, 170, 170, 0, 340, 8),
            ANIMATION_MOVE: AnimationParams(sheet, 6, 1, 170, 170, 0, 510, 8),
            ANIMATION_END_MOVE: AnimationParams(sheet, 6, 1, 170, 170, 0, 680, 1),
            ANIMATION_DEATH: AnimationParams(sheet, 6, 1, 170, 170, 0, 680, 8)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, ['music', 'dragon_hit.wav'],
                         death_callback, mirror_animation)  # анимации дракона
        self.init_stats(4, 2, MELEE_ATTACK, 200, 30, UNIT_DRAGON, 'Дракон', QUANTITY_DRAGON)


def set_view_stock(screen, coords, size):  # отображение количества лучников
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
