import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name_unit, x, y, step, distance_attack, hp, damage, image, image_size, group):
        super().__init__(group)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((0xb3, 0x22, 0xb7))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.step = step
        self.distance_attack = distance_attack
        self.hp = hp
        self.damage = damage
        self.name = name_unit


swordsmans = pygame.sprite.Group()
archers = pygame.sprite.Group()
cavalrys = pygame.sprite.Group()
dragons = pygame.sprite.Group()
castles = pygame.sprite.Group()
