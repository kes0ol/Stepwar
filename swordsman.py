import pygame


class Swordsman(pygame.sprite.Sprite):

    def __init__(self, x, y, cell_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/swordsman.jpeg')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


swordsmans = pygame.sprite.Group()
