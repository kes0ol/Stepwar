import pygame


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, image_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/grass.jpeg')
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


grasses = pygame.sprite.Group()
