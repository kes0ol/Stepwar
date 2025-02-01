import pygame

from animation import AnimationParams
from global_vars import ANIMATION_ATTACK, ANIMATION_IDLE, ANIMATION_MOVE, ANIMATION_BEGIN_MOVE, ANIMATION_END_MOVE, \
    ANIMATION_DEATH, MELEE_ATTACK
from unit import Unit


class Dragon(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/dragon.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 4, 1, 125, 125, 0, 0, 10),
            ANIMATION_ATTACK: AnimationParams(sheet, 7, 1, 170, 170, 0, 170, 8),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 3, 1, 170, 170, 0, 340, 8),
            ANIMATION_MOVE: AnimationParams(sheet, 6, 1, 170, 170, 0, 510, 8),
            ANIMATION_END_MOVE: AnimationParams(sheet, 6, 1, 170, 170, 0, 680, 8),
            ANIMATION_DEATH: AnimationParams(sheet, 6, 1, 170, 170, 0, 680, 8)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(4, 2, MELEE_ATTACK, 150, 30, 'dragon', 'Дракон', 2)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
