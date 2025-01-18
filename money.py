import pygame


class Money(pygame.sprite.Sprite):

    def __init__(self, x, y, image_size, group):
        super().__init__(group)
        self.image = pygame.image.load('images/money.png')
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image.set_colorkey((0xb3, 0x22, 0xb7))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def render(self, screen, money):
        moneys.draw(screen)

        font = pygame.font.Font(None, 50)
        text = font.render(f'{money}', True, 'yellow')
        screen.blit(text, (self.rect.x - 50, self.rect.y))


moneys = pygame.sprite.Group()
