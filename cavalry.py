import pygame


class Cavalry(pygame.sprite.Sprite):

    def __init__(self, x, y, image_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/cavalry.jpeg')
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = 4


stock = 5


def set_view_stock(screen, coords):
    font = pygame.font.Font(None, 50)
    text = font.render(f'{stock}', True, 'white')
    screen.blit(text, (coords[0], coords[1]))


cavalrys = pygame.sprite.Group()
