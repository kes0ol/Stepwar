import os
import pygame

from internal.different.animation import AnimationChain, MovableAnimatedSprite
from internal.different.global_vars import ANIMATION_ATTACK, ANIMATION_IDLE, ANIMATION_MOVE, \
    ANIMATION_END_MOVE, ANIMATION_BEGIN_MOVE, RANGE_ATTACK, MELEE_ATTACK, ANIMATION_DEATH, BOARD_EMPTY, FIELD_HILL, \
    UNIT_CAVALRY, UNIT_DRAGON


class Unit(MovableAnimatedSprite):
    '''Класс юнитов'''
    def __init__(self, animations, x, y, group, scale_to, default_animation, hit_sound, death_callback,
                 mirror_animation=False):
        '''Инициализация класса'''
        super().__init__(animations, x, y, group, scale_to, default_animation, mirror_animation)
        self.death_callback = death_callback
        self.default_stock = 0

        self.default_step = 0
        self.step = 0
        self.do_damage = True
        self.is_dead = False

        self.distance_attack = 0
        self.attack_type = MELEE_ATTACK
        self.hp = 0
        self.damage = 0
        self.damage_plus = 0
        self.name = ''
        self.title = ''

        self.hit_sound = pygame.mixer.Sound(os.path.join(*hit_sound))
        self.death_sound = pygame.mixer.Sound(os.path.join('music', 'kill_hit.wav'))

    def __repr__(self):
        '''Функция для отображения информации о классе'''
        return f"[{id(self)} | {super().__repr__()}]"

    def init_stats(self, step, distance_attack, attack_type, hp, damage, name, title, stock):
        '''Характеристики юнитов'''
        self.default_step = step
        self.step = step
        self.distance_attack = distance_attack
        self.attack_type = attack_type
        self.hp = hp
        self.damage = damage
        self.name = name
        self.title = title
        self.default_stock = stock

    def update(self, *args, **kwargs):
        '''Функция для изменения кадра анимации и его положения на экране'''
        self.next_frame()
        self.move_tick()
        self.gc_tick()

    def make_step(self, cell_coords, choose_cell, screen, callback=None, callback_args=None):
        '''Функция для перехода на другую клетку'''
        x_now, y_now = cell_coords
        select_x, select_y = choose_cell
        self.damage_plus = 0

        if screen.board.field[select_y][select_x] == FIELD_HILL:
            if self.name not in (UNIT_CAVALRY, UNIT_DRAGON):
                self.step -= 1
                if self.attack_type == RANGE_ATTACK:
                    self.damage_plus = 15

        screen.board.board[y_now][x_now], screen.board.board[select_y][select_x] = screen.board.board[select_y][
            select_x], screen.board.board[y_now][x_now]

        x = (select_x - x_now) * screen.board.cell_size
        y = (select_y - y_now) * screen.board.cell_size
        px = self.rect.x + x
        py = self.rect.y + y

        mirror = x < 0
        animation_chain = AnimationChain()
        animation_chain.add_step(ANIMATION_BEGIN_MOVE, mirror=mirror)
        steps = max([abs(select_x - x_now), abs(select_y - y_now)])

        tx = x / steps
        ty = y / steps
        for i in range(1, steps + 1):
            animation_chain.add_step(ANIMATION_MOVE, self.move, [tx, ty], mirror=mirror)

        animation_chain.add_step(ANIMATION_END_MOVE, self.set_position, [px, py], mirror=mirror)
        animation_chain.add_step(ANIMATION_IDLE, callback, callback_args)

        self.start_animation_chain(animation_chain)

        self.step -= (abs(x // screen.board.cell_size) + abs(y // screen.board.cell_size))

    def make_attack(self, unit, choose_cell, screen, callback=None, callback_args=None):
        '''Функция для атаки'''
        animation_chain = AnimationChain()

        x, _ = screen.board.get_cell_coords(choose_cell)
        mirror = x < self.rect.x
        args = [screen, unit]
        animation_chain.add_step(ANIMATION_ATTACK, self.give_damage, args, mirror=mirror)
        self.hit_sound.play()
        animation_chain.add_step(ANIMATION_IDLE, callback, callback_args)

        self.start_animation_chain(animation_chain)
        self.do_damage = False

    def make_death(self):
        '''Запуск анимации смерти юнита'''
        animation_chain = AnimationChain()

        animation_chain.add_step(ANIMATION_IDLE)
        animation_chain.add_step(ANIMATION_DEATH)
        self.death_sound.play()
        animation_chain.add_step(ANIMATION_DEATH, self.kill, [])

        self.start_animation_chain(animation_chain)

    def recieve_damage(self, actor):
        '''Функция для получения урона от атакующего юнита'''
        self.hp -= actor.get_damage()
        if self.hp <= 0:
            self.is_dead = True
            self.make_death()

    def get_damage(self):
        '''Возвращение текущего урона'''
        return self.damage + self.damage_plus

    def give_damage(self, screen, unit):
        '''Нанесение урона по юниту'''
        unit.recieve_damage(self)
        if unit.is_dead:  # удаление убитого юнита
            for i in range(screen.board.height):
                for j in range(screen.board.width):
                    if unit.rect.collidepoint(screen.board.get_cell_coords((j, i))):
                        screen.board.board[i][j] = BOARD_EMPTY

            self.death_callback(screen, unit, self)

    def refresh(self):
        '''Восстановить ходы на следующем ходе'''
        self.step = self.default_step
        self.do_damage = True
