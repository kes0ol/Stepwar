import pygame

import start_game


class Dragon(pygame.sprite.Sprite):

    def __init__(self, x, y, image_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/dragon.xcf')
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image.set_colorkey((0xb3, 0x22, 0xb7))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = 4
        self.do_damage = True
        self.distance_attack = 2
        self.stock = 1
        self.hp = 150
        self.damage = 30
        self.damage_plus = 0
        self.name = 'dragon'

    def update(self, *args, **kwargs):
        self.x_now, self.y_now = args[0]
        self.select_y, self.select_x = args[1]
        self.screen = args[2]
        self.is_attack = args[3]
        self.damage_plus = 0

        if not self.is_attack:
            self.screen.board.board[self.y_now][self.x_now] = 0
            self.screen.board.board[self.select_y][self.select_x] = 1

            x = (self.select_x - self.x_now) * self.screen.board.cell_size
            y = (self.select_y - self.y_now) * self.screen.board.cell_size

            self.rect = self.rect.move(x, y)
        else:
            start_game.give_damage(self.screen, (
                self.select_x * self.screen.board.cell_size + self.screen.board.left,
                self.select_y * self.screen.board.cell_size + self.screen.board.top), (self.select_x, self.select_y),
                                   self.damage + self.damage_plus)


def set_view_stock(screen, coords):
    font = pygame.font.Font(None, 50)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, coords)


stock = None
dragons = pygame.sprite.Group()
