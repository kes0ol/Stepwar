import os

import pygame

from development.different.animation import AnimationParams
from development.different.global_vars import ANIMATION_IDLE, MELEE_ATTACK, ANIMATION_DEATH

from development.units.unit import Unit


class Castle(Unit):
    def __init__(self, x, y, image_size, group, damage_func=True, mirror_animation=False):
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'castle.png'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, -1),
            ANIMATION_DEATH: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, 1),
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, damage_func, mirror_animation)
        self.init_stats(0, 0, MELEE_ATTACK, 500, 0, 'castle', 'Замок', 0)
