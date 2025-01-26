import pygame

import start_game
from animation import AnimatedSprite, AnimationParams

# def start_move_callback


class BoneDragon(AnimatedSprite):
    def __init__(self, x, y, image_size, group):
        sheet = pygame.image.load('images/team_images/bone_dragon3.png')
        animations = {
            "idle": AnimationParams(sheet, 4, 1, 125, 125, 0, 0, 30),
            "attack": AnimationParams(sheet, 7, 1, 170, 170, 0, 170, 10),
            "start_move": AnimationParams(sheet, 3, 1, 170, 170, 0, 340, 10),
            "move": AnimationParams(sheet, 6, 1, 170, 170, 0, 510, 10),
            "stop_move": AnimationParams(sheet, 6, 1, 170, 170, 0, 680, 10)
        }
        super().__init__(animations, x, y, group, image_size, "idle")
        self.step = 4
        self.do_damage = True
        self.distance_attack = 2
        self.stock = 2
        self.hp = 150
        self.damage = 30
        self.damage_plus = 0
        self.name = 'dragon'
        self.title = 'Дракон'


    def update(self, *args, **kwargs):
        self.next()


    def choose_step(self, cell_coords, choose_cell, screen, is_attack):
        self.x_now, self.y_now = cell_coords
        self.select_y, self.select_x = choose_cell
        # self.screen = screen
        self.is_attack = is_attack
        self.damage_plus = 0

        if screen.board.field[self.select_y][self.select_x] == 2:
            self.damage_plus = 15

        if not self.is_attack:
            screen.board.board[self.y_now][self.x_now] = 0
            screen.board.board[self.select_y][self.select_x] = 1

            x = (self.select_x - self.x_now) * screen.board.one_size
            y = (self.select_y - self.y_now) * screen.board.one_size

            self.rect = self.rect.move(x, y)
        else:
            start_game.give_damage(screen, (
                self.select_x * screen.board.one_size + screen.board.left,
                self.select_y * screen.board.one_size + screen.board.top), (self.select_x, self.select_y),
                                   self.damage + self.damage_plus)


def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
archers = pygame.sprite.Group()
