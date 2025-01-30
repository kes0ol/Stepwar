import pygame

import start_game
from animation import AnimationParams
from global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, ANIMATION_MOVE, ANIMATION_END_MOVE, \
    ANIMATION_DEATH, MELEE_ATTACK
from unit import Unit


# class Swordsman(pygame.sprite.Sprite):
#
#     def __init__(self, x, y, image_size, group):
#         super().__init__(group)
#         self.image = pygame.image.load('images/team_images/swordsman.png')
#         self.image = pygame.transform.scale(self.image, (image_size, image_size))
#         self.image.set_colorkey((0xb3, 0x22, 0xb7))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.step = 2
#         self.do_damage = True
#         self.distance_attack = 1
#         self.stock = 4
#         self.hp = 100
#         self.damage = 20
#         self.damage_plus = 0
#         self.name = 'swordsman'
#         self.title = 'Рыцарь'
#
#     def update(self, *args, **kwargs):
#         self.x_now, self.y_now = args[0]
#         self.select_y, self.select_x = args[1]
#         self.screen = args[2]
#         self.is_attack = args[3]
#         self.damage_plus = 0
#
#         if not self.is_attack:
#             self.screen.board.board[self.y_now][self.x_now] = 0
#             self.screen.board.board[self.select_y][self.select_x] = 1
#
#             x = (self.select_x - self.x_now) * self.screen.board.cell_size
#             y = (self.select_y - self.y_now) * self.screen.board.cell_size
#
#             self.rect = self.rect.move(x, y)
#         else:
#             start_game.give_damage(self.screen, (
#                 self.select_x * self.screen.board.cell_size + self.screen.board.left,
#                 self.select_y * self.screen.board.cell_size + self.screen.board.top), (self.select_x, self.select_y),
#                                    self.damage + self.damage_plus)

class Swordsman(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/Crusader.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 5, 1, 100, 100, 0, 0, 15),
            ANIMATION_ATTACK: AnimationParams(sheet, 7, 1, 100, 100, 0, 100, 15),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 15),
            ANIMATION_MOVE: AnimationParams(sheet, 5, 1, 100, 100, 0, 200, 15),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 15),
            ANIMATION_DEATH: AnimationParams(sheet, 6, 1, 100, 100, 0, 300, 15)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(2, 1, MELEE_ATTACK, 10, 20, 'swordsman', 'Рыцарь', 1)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
# swordsmans = pygame.sprite.Group()
