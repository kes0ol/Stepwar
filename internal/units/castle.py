import os

import pygame

from internal.different.animation import AnimationParams
from internal.different.global_vars import ANIMATION_IDLE, MELEE_ATTACK, ANIMATION_DEATH, UNIT_CASTLE
from internal.units.unit import Unit


class Castle(Unit):
    '''Создание класса замка'''
    def __init__(self, x, y, image_size, group, death_callback, mirror_animation=False):
        '''Инициализация класса'''
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'castle.png'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, -1),
            ANIMATION_DEATH: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, 1),
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE,
                         ['music', 'kill_hit.wav'], death_callback, mirror_animation)
        self.init_stats(0, 0, MELEE_ATTACK, 250, 0, UNIT_CASTLE, 'Замок')
