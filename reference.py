import sys

import pygame
import mapping
import swordsman, archer, castle, cavalry, dragon
import landscapes

from widgets import Button


class Reference_window(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.ref_screen = Description(self.main_screen, self.size, self.main)
        self.next_page_button = Button('->', 200, self.width - 80, self.height - 80,
                                       color=(100, 0, 0), dark_color=(50, 0, 0))
        self.back_button = Button('Назад', 80, 120, self.height - 70, color=(100, 0, 0), dark_color=(50, 0, 0))
        self.lst_buttons = [self.back_button, self.next_page_button]

        t = ('''Игра представляет из себя стратегию, состоящую из уровней.Каждый юнит обладает уникальными
             характеристиками, такие как: урон, дальность атаки, дальность передвижения и другими атрибутами. После
             расстановки юнитов нажмите "Начать игру" и управляйте своими юнитами, а так же пробуйте вступать в схватку
             с противником. Перед тем как начать игру, вы можете расставить своих юнитов, нажимая на иконку слева от 
             поля битвы и кликая на клетку поля. За пройденный уровень вы получаете очки. Чтобы пройти уровень, нужно
             сокрушить вражеский замок. С каждым пройденным уровнем вы получаете доступ к следующему.''')

        self.lst = self.parse_text(t, self.one_size)

        self.fon = pygame.image.load('images/backgrounds/reffon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

    def parse_text(self, text, width):
        lst = text.split()
        res = []
        w = width
        st = ''
        while len(lst) > 1:
            while w > 0 and len(lst) > 1:
                if len(lst[0]) > 0:
                    st += lst[0] + ' '
                    lst = lst[1:]
                    w -= len(lst[0])
                else:
                    break
            w = width
            res.append(st)
            st = ''
        return res

    def check_click(self, mouse_pos, lst):
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.next_page_button:
                    self.ref_screen.start()
                if button == self.back_button:
                    self.running = False

    def render(self):
        y = round(self.one_size / 1.7)
        self.main_screen.sc.blit(self.fon, (0, 0))
        for i in self.lst:
            font = pygame.font.Font(None, self.one_size // 2)
            text = font.render(i, True, 'black')
            self.main_screen.sc.blit(text, (self.width / 25, self.one_size + y))
            y += round(self.one_size / 1.7)
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.render_cursor()

    def start(self):
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()


class Description(mapping.Window):
    def __init__(self, screen, size, main):
        super().__init__(screen, size, main)
        self.back_button = Button('<-', round(self.one_size * 2.4), self.one_size,
                                  self.height - self.one_size, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.swordsman_button = Button('Рыцарь', round(self.one_size * 1.2), self.one_size * 3,
                                       self.one_size, color=(100, 0, 0),
                                       dark_color=(50, 0, 0))
        self.archer_button = Button('Лучник', round(self.one_size * 1.2), self.one_size * 3,
                                    round(self.one_size * 2.5), color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.cavalry_button = Button('Кавалерия', round(self.one_size * 1.2), self.one_size * 3,
                                     self.one_size * 4, color=(100, 0, 0),
                                     dark_color=(50, 0, 0))
        self.dragon_button = Button('Дракон', round(self.one_size * 1.2), self.one_size * 3,
                                    round(self.one_size * 5.5), color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.castle_button = Button('Замок', round(self.one_size * 1.2), self.one_size * 3,
                                    self.one_size * 7, color=(100, 0, 0),
                                    dark_color=(50, 0, 0))
        self.grass_button = Button('Трава', round(self.one_size * 1.2), self.one_size * 8,
                                   self.one_size, color=(100, 0, 0),
                                   dark_color=(50, 0, 0))
        self.rock_button = Button('Гора', round(self.one_size * 1.2), self.one_size * 8,
                                  round(self.one_size * 2.5), color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.hill_button = Button('Холм', round(self.one_size * 1.2), self.one_size * 8,
                                  self.one_size * 4, color=(100, 0, 0),
                                  dark_color=(50, 0, 0))
        self.river_button = Button('Река', round(self.one_size * 1.2), self.one_size * 8,
                                   round(self.one_size * 5.5), color=(100, 0, 0),
                                   dark_color=(50, 0, 0))

        self.icons_units = pygame.sprite.Group()

        self.lst_buttons = [self.back_button, self.swordsman_button, self.archer_button, self.cavalry_button,
                            self.dragon_button, self.castle_button, self.grass_button, self.rock_button,
                            self.hill_button, self.river_button]

        self.dct_units = {self.swordsman_button: swordsman.Swordsman,
                          self.archer_button: archer.Archer,
                          self.cavalry_button: cavalry.Cavalry,
                          self.dragon_button: dragon.Dragon,
                          self.castle_button: castle.Castle}

        self.dct_lands = {self.grass_button: ('grass', 'Трава', self.one_size * 17, self.height // 2,
                                              'images/landscapes/grass.png', self.one_size * 4, 0, 0,
                                              self.icons_units),
                          self.rock_button: ('mountains', 'Гора', self.one_size * 17, self.height // 2,
                                             'images/landscapes/mountains.png', self.one_size * 4, 0, 'нельзя',
                                             self.icons_units),
                          self.hill_button: ('hill', 'Холм', self.one_size * 17, self.height // 2,
                                             'images/landscapes/hill.png', self.one_size * 4, 15, -1,
                                             self.icons_units),
                          self.river_button: ('river', 'Река', self.one_size * 17, self.height // 2,
                                              'images/landscapes/river.png', self.one_size * 4, 0, 'Частично',
                                              self.icons_units)}

        self.stats = []

        self.fon = pygame.image.load('images/backgrounds/reffon.jpg')
        self.fon = pygame.transform.scale(self.fon, (self.width, self.height))

    def check_click(self, mouse_pos, lst):
        self.icons_units.empty()
        for button in lst:
            if button.check_click(mouse_pos):
                if button == self.back_button:
                    self.running = False
                elif button in self.dct_units.keys():
                    self.icon_unit = self.dct_units[button](self.one_size * 17, self.height // 2,
                                                            self.one_size * 4, self.icons_units)
                    self.stats = [f'Тип юнита: {self.icon_unit.title}',
                                  f'Здоровье: {self.icon_unit.hp}',
                                  f'Урон: {self.icon_unit.damage}',
                                  f'Передвижение: {self.icon_unit.step}',
                                  f'Дистанция атаки: {self.icon_unit.distance_attack}']
                elif button in self.dct_lands.keys():
                    self.icon_land = landscapes.Landscape(*self.dct_lands[button])
                    self.stats = [
                        f'Ландшафт: {self.icon_land.title}',
                        f'Доп. урон: {self.icon_land.damage}',
                        f'Передвижение: {self.icon_land.move}']

    def render(self):
        y = 50
        self.main_screen.sc.blit(self.fon, (0, 0))
        pygame.draw.rect(self.main_screen.sc, (66, 44, 33), (self.width // 2, self.height // 3, self.one_size * 12,
                                                          self.one_size * 12), 8)
        f = pygame.font.Font(None, 100)
        t = f.render('Информация', True, 'black')
        self.main_screen.sc.blit(t, (self.one_size * 12, self.height / 2.8))
        if len(self.icons_units):
            pygame.draw.rect(self.main_screen.sc, (0, 0, 0), (self.one_size * 17 - 5, self.height // 2 - 5,
                                                              self.one_size * 4 + 10, self.one_size * 4 + 10), 8)
            self.icons_units.draw(self.main_screen.sc)
            for i in reversed(self.stats):
                font = pygame.font.Font(None, 40)
                text = font.render(i, True, 'black')
                self.main_screen.sc.blit(text, (self.one_size * 12, self.height / 1.3 - y))
                y += 50
        for button in self.lst_buttons:
            button.render(self.main_screen.sc)
        self.main_screen.render_cursor()

    def start(self):
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos, self.lst_buttons)

            self.main_screen.sc.fill((0, 0, 0))
            self.render()

            clock.tick(fps)
            pygame.display.flip()
