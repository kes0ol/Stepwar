import os

import pygame

from internal.different.animation import AnimationParams
from internal.different.global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, \
    ANIMATION_MOVE, ANIMATION_END_MOVE, ANIMATION_DEATH, RANGE_ATTACK, UNIT_ARCHER
from internal.units.unit import Unit


class Archer(Unit):
    '''Создание класса лучника'''
    def __init__(self, x, y, image_size, group, death_callback, mirror_animation=False):
        '''Инициализация класса'''
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'archer.png'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 4, 1, 100, 100, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 8, 1, 100, 100, 0, 100, 5),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 5),
            ANIMATION_MOVE: AnimationParams(sheet, 12, 1, 100, 100, 0, 200, 4),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 1),
            ANIMATION_DEATH: AnimationParams(sheet, 11, 1, 100, 100, 0, 300, 5)
        } # анимации лучника
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, ['music', 'archer_hit.wav'],
                         death_callback, mirror_animation)
        self.init_stats(1, 3, RANGE_ATTACK, 40, 30, UNIT_ARCHER, 'Лучник', 2)


def set_view_stock(screen, coords, size): # отображение количества лучников
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
