import pygame

import start_game
from animation import MovableAnimatedSprite, AnimationParams, AnimationChain

class BoneDragon(MovableAnimatedSprite):
    def __init__(self, x, y, image_size, group, ):
        sheet = pygame.image.load('images/team_images/bone_dragon.png')
        animations = {
            "idle": AnimationParams(sheet, 4, 1, 125, 125, 0, 0, 40),
            "attack": AnimationParams(sheet, 7, 1, 170, 170, 0, 170, 10),
            "start_move": AnimationParams(sheet, 3, 1, 170, 170, 0, 340, 15),
            "move": AnimationParams(sheet, 6, 1, 170, 170, 0, 510, 15),
            "stop_move": AnimationParams(sheet, 6, 1, 170, 170, 0, 680, 20)
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
        self.next_frame()
        self.move_tick()
        self.gc_tick()

    def choose_step(self, cell_coords, choose_cell, screen, is_attack):
        x_now, y_now = cell_coords
        select_y, select_x = choose_cell
        self.is_attack = is_attack
        self.damage_plus = 0

        if screen.board.field[select_y][select_x] == 2:
            self.damage_plus = 15

        if not self.is_attack:
            screen.board.board[y_now][x_now] = 0
            screen.board.board[select_y][select_x] = 1

            x = (select_x - x_now) * screen.board.cell_size
            y = (select_y - y_now) * screen.board.cell_size
            px = self.rect.x + x
            py = self.rect.y + y

            mirror = x < 0
            animation_chain = AnimationChain()
            animation_chain.add_step("start_move", mirror=mirror)
            steps = max([abs(select_x - x_now), abs(select_y - y_now)])
            tx = x / steps
            ty = y / steps
            for i in range(1, steps + 1):
                animation_chain.add_step("move", self.move, [tx, ty], mirror=mirror)
            animation_chain.add_step("stop_move", self.set_position, [px, py], mirror=mirror)
            animation_chain.add_step("idle")

            self.start_animation_chain(animation_chain)
        else:
            start_game.give_damage(screen, (
                select_x * screen.board.cell_size + screen.board.left,
                select_y * screen.board.cell_size + screen.board.top), (select_x, select_y),
                                   self.damage + self.damage_plus)





def set_view_stock(screen, coords, size):
    font = pygame.font.Font(None, size)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
archers = pygame.sprite.Group()
