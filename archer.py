import pygame

from animation import AnimationParams
from global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, ANIMATION_MOVE, ANIMATION_END_MOVE, \
    ANIMATION_DEATH, RANGE_ATTACK
from unit import Unit


class Archer(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/archer.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 4, 1, 100, 100, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 8, 1, 100, 100, 0, 100, 8),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 8),
            ANIMATION_MOVE: AnimationParams(sheet, 12, 1, 100, 100, 0, 200, 8),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 8),
            ANIMATION_DEATH: AnimationParams(sheet, 11, 1, 100, 100, 0, 300, 8)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(1, 3, RANGE_ATTACK, 40, 30, 'archer', 'Лучник', 4)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
