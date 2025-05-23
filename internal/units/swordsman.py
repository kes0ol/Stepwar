import os

import pygame

from internal.different.animation import AnimationParams
from internal.different.global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, \
    ANIMATION_MOVE, ANIMATION_END_MOVE, ANIMATION_DEATH, MELEE_ATTACK, UNIT_SWORDSMAN, QUANTITY_SWORDSMAN
from internal.units.unit import Unit


class Swordsman(Unit):
    '''Создание класса рыцаря'''

    def __init__(self, x, y, image_size, group, death_callback, mirror_animation=False):
        '''Инициализация класса'''
        sheet = pygame.image.load(os.path.join('images', 'team_images', 'swordsman.jpg'))
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 5, 1, 100, 100, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 7, 1, 100, 100, 0, 100, 5),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 5),
            ANIMATION_MOVE: AnimationParams(sheet, 5, 1, 100, 100, 0, 200, 7),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 1),
            ANIMATION_DEATH: AnimationParams(sheet, 6, 1, 100, 100, 0, 300, 10)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, ['music', 'swordsman_hit.wav'],
                         death_callback, mirror_animation)  # анимации рыцаря
        self.init_stats(2, 1, MELEE_ATTACK, 80, 20, UNIT_SWORDSMAN, 'Рыцарь', QUANTITY_SWORDSMAN)


def set_view_stock(screen, coords, size):  # отображение количества лучников
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
