import pygame

from animation import AnimationParams
from global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, ANIMATION_MOVE, ANIMATION_END_MOVE, \
    ANIMATION_DEATH, MELEE_ATTACK
from unit import Unit


class Swordsman(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/swordsman.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 5, 1, 100, 100, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 7, 1, 100, 100, 0, 100, 15),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 15),
            ANIMATION_MOVE: AnimationParams(sheet, 5, 1, 100, 100, 0, 200, 15),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 15),
            ANIMATION_DEATH: AnimationParams(sheet, 6, 1, 100, 100, 0, 300, 15)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(2, 1, MELEE_ATTACK, 100, 20, 'swordsman', 'Рыцарь', 5)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
