import pygame

from animation import AnimationParams
from global_vars import ANIMATION_IDLE, MELEE_ATTACK, ANIMATION_DEATH
from unit import Unit


# class Castle(pygame.sprite.Sprite):
#
#     def __init__(self, x, y, cell_size, group):
#         super().__init__(group)
#         self.image = pygame.image.load('images/team_images/castle.png')
#         self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#         self.step = 0
#         self.do_damage = True
#         self.distance_attack = 0
#         self.hp = 500
#         self.damage = 0
#         self.damage_plus = 0
#         self.name = 'castle'
#         self.title = 'Замок'


class Castle(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/castle.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, -1),
            ANIMATION_DEATH: AnimationParams(sheet, 1, 1, 225, 225, 0, 0, 1),
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(0, 0, MELEE_ATTACK, 5, 0, 'castle', 'Замок', 0)


# def add_start_castle(x, y, cell_size):
#     Castle(x, y, cell_size * 2, my_units_group)


# castles = pygame.sprite.Group()
