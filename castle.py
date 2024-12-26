import pygame


class Castle(pygame.sprite.Sprite):

    def __init__(self, x, y, cell_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/castle.jpeg')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def add_start_castle(x, y, cell_size):
    Castle(x, y, cell_size, castles)


castles = pygame.sprite.Group()
