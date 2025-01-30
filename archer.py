import pygame

import start_game
from animation import AnimationParams
from global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, ANIMATION_MOVE, ANIMATION_END_MOVE, \
    ANIMATION_DEATH, MELEE_ATTACK, RANGE_ATTACK
from unit import Unit


# class Archer(pygame.sprite.Sprite):
#
#     def __init__(self, x, y, image_size, group):
#         super().__init__(group)
#         self.image = pygame.image.load('images/team_images/archer.png')
#         self.image = pygame.transform.scale(self.image, (image_size, image_size))
#         self.image.set_colorkey((0xb3, 0x22, 0xb7))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.step = 1
#         self.do_damage = True
#         self.distance_attack = 3
#         self.stock = 2
#         self.hp = 40
#         self.damage = 30
#         self.damage_plus = 0
#         self.name = 'archer'
#         self.title = 'Лучник'
#
#     def choose_step(self, cell_coords, choose_cell, screen, is_attack):
#         self.x_now, self.y_now = cell_coords
#         self.select_y, self.select_x = choose_cell
#         self.screen = screen
#         self.is_attack = is_attack
#         self.damage_plus = 0
#
#         if self.screen.board.field[self.select_y][self.select_x] == 2:
#             self.damage_plus = 15
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
class Archer(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/Sharpshooter.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 4, 1, 100, 100, 0, 0, 15),
            ANIMATION_ATTACK: AnimationParams(sheet, 8, 1, 100, 100, 0, 100, 15),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 10),
            ANIMATION_MOVE: AnimationParams(sheet, 12, 1, 100, 100, 0, 200, 10),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 100, 100, 0, 0, 10),
            ANIMATION_DEATH: AnimationParams(sheet, 11, 1, 100, 100, 0, 300, 15)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(1, 3, RANGE_ATTACK, 40, 30, 'archer', 'Лучник', 4)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
# archers = pygame.sprite.Group()
