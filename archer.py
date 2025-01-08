import pygame

import start_game


class Archer(pygame.sprite.Sprite):

    def __init__(self, x, y, image_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/archer.png')
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image.set_colorkey((0xb3, 0x22, 0xb7))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = 1
        self.do_damage = True
        self.distance_attack = 3
        self.stock = 8
        self.hp = 40
        self.damage = 30

    def update(self, *args, **kwargs):
        self.x_now, self.y_now = args[0]
        self.select_y, self.select_x = args[1]
        self.screen = args[2]
        self.is_attack = args[3]

        if not self.is_attack:
            self.screen.board.board[self.y_now][self.x_now] = 0
            self.screen.board.board[self.select_y][self.select_x] = 1

            self.x = (self.select_x - self.x_now) * self.screen.board.cell_size
            self.y = (self.select_y - self.y_now) * self.screen.board.cell_size

            self.rect = self.rect.move(self.x, self.y)
        else:
            start_game.give_damage(self.screen, (
                self.select_x * self.screen.board.cell_size + self.screen.board.left,
                self.select_y * self.screen.board.cell_size + self.screen.board.top), (self.select_x, self.select_y),
                                   self.damage)


def set_view_stock(screen, coords):
    font = pygame.font.Font(None, 50)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, (coords[0], coords[1]))


stock = None
archers = pygame.sprite.Group()
