import pygame


class Landscape(pygame.sprite.Sprite):
    '''Класс для создания ландшафтов'''

    def __init__(self, name, title, x, y, image, image_size, damage, move, group):
        '''Инициализация класса'''
        super().__init__(group)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image.set_colorkey((0xb3, 0x22, 0xb7))

        self.name = name
        self.title = title
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.damage = damage
        self.move = move
