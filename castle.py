import pygame

from animation import AnimationParams
from global_vars import ANIMATION_IDLE, MELEE_ATTACK, ANIMATION_DEATH
from unit import Unit


class Castle(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/castle.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, -1),
            ANIMATION_DEATH: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, 1),
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(0, 0, MELEE_ATTACK, 500, 0, 'castle', 'Замок', 0, 'music/archer_hit.wav')
