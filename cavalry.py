import pygame

import start_game
from animation import AnimationParams
from global_vars import ANIMATION_IDLE, ANIMATION_ATTACK, ANIMATION_BEGIN_MOVE, ANIMATION_MOVE, ANIMATION_END_MOVE, \
    ANIMATION_DEATH, MELEE_ATTACK
from unit import Unit


# class Cavalry(pygame.sprite.Sprite):
#
#     def __init__(self, x, y, image_size, group):
#         super().__init__(group)
#         self.image = pygame.image.load('images/team_images/cavalry.png')
#         self.image = pygame.transform.scale(self.image, (image_size, image_size))
#         self.image.set_colorkey((0xb3, 0x22, 0xb7))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.step = 3
#         self.do_damage = True
#         self.distance_attack = 1
#         self.stock = 0
#         self.hp = 70
#         self.damage = 25
#         self.damage_plus = 0
#         self.name = 'cavalry'
#         self.title = 'Кавалерия'
#
#     def choose_step(self, cell_coords, choose_cell, screen, is_attack):
#         self.x_now, self.y_now = cell_coords
#         self.select_y, self.select_x = choose_cell
#         self.screen = screen
#         self.is_attack = is_attack
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

class Cavalry(Unit):
    def __init__(self, x, y, image_size, group, mirror_animation=False):
        sheet = pygame.image.load('images/team_images/Champion.png')
        animations = {
            ANIMATION_IDLE: AnimationParams(sheet, 9, 1, 130, 130, 0, 0, 15),
            ANIMATION_ATTACK: AnimationParams(sheet, 9, 1, 130, 130, 0, 130, 15),
            ANIMATION_BEGIN_MOVE: AnimationParams(sheet, 1, 1, 130, 130, 0, 0, 15),
            ANIMATION_MOVE: AnimationParams(sheet, 7, 1, 130, 130, 0, 0, 15),
            ANIMATION_END_MOVE: AnimationParams(sheet, 1, 1, 130, 130, 0, 0, 15),
            ANIMATION_DEATH: AnimationParams(sheet, 8, 1, 130, 130, 0, 390, 15)
        }
        super().__init__(animations, x, y, group, image_size, ANIMATION_IDLE, mirror_animation)
        self.init_stats(3, 1, MELEE_ATTACK, 70, 25, 'cavalry', 'Кавалерия', 3)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
# cavalrys = pygame.sprite.Group()
