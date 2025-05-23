import random

import pygame

from internal.different.global_vars import ANIMATION_IDLE


class AnimationParams:
    '''Создание класса параметров анимаций'''

    def __init__(self, sheet, columns, rows, w, h, ltop_x, ltop_y, fps_mod):
        '''Инициализация класса'''
        self.sheet = sheet
        self.columns = columns
        self.rows = rows
        self.w, self.h = w, h
        self.ltop_x, self.ltop_y = ltop_x, ltop_y
        self.fps_mod = fps_mod


class AnimationStep:
    '''Структурный Класс для шагов анимации'''

    def __init__(self, animation, action, action_args, mirror):
        '''Инициализация класса'''
        self.animation = animation
        self.action = action
        self.action_args = action_args
        self.mirror = mirror


class AnimationChain:
    '''Класс цепочки анимаций'''

    def __init__(self):
        '''Инициализация класса'''
        self.steps = []

    def add_step(self, animation, action=None, action_args=None, mirror=False):
        '''Добавление шага'''
        self.steps.append(AnimationStep(animation, action, action_args, mirror))

    def __iter__(self):
        '''Генератор для итерирования по шагам'''
        for i in reversed(self.steps):
            yield i


class AnimatedSprite(pygame.sprite.Sprite):
    '''Класс для анимации'''

    def __init__(self, animations, x, y, group, scale_to, default_animation, mirror_animation=False):
        '''Инициализация класса'''
        super().__init__(group)
        self.scale_to = scale_to
        self.rect = pygame.Rect(0, 0, scale_to, scale_to)
        self.rect = self.rect.move(x, y)
        self.frames = dict()
        self.animations = animations
        for k, v in animations.items():
            mirror = k == ANIMATION_IDLE and mirror_animation
            self.frames[k] = self.cut_sheet(v.sheet, v.columns, v.rows, v.w, v.h, v.ltop_x, v.ltop_y, mirror)
        self.current_animation = default_animation
        self.frame_idx = 0
        self.image = self.frames[self.current_animation][0]
        self.mirror_current_animation = False
        self.mirror_animation = mirror_animation
        self.callback = None
        self.gc = 0 + random.randint(0, 10)

    def cut_sheet(self, sheet, columns, rows, w, h, ltop_x, ltop_y, mirror):
        '''Фунция для разрезания картинки на кадры'''
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (ltop_x + w * i, ltop_y + h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, (w, h)))

                image = pygame.transform.scale(image, (self.scale_to, self.scale_to))
                if mirror:
                    image = pygame.transform.flip(image, True, False)
                frames.append(image)
        return frames

    def next_frame(self):
        '''Переключение кадра анимации'''
        if self.gc % self.animations[self.current_animation].fps_mod == 0:
            self.frame_idx += 1
            if self.frame_idx == len(self.frames[self.current_animation]) and self.callback is not None:
                self.callback()
            self.frame_idx %= len(self.frames[self.current_animation])
            self.image = self.frames[self.current_animation][self.frame_idx]
            if self.mirror_current_animation:
                self.image = pygame.transform.flip(self.image, True, False)

    def gc_tick(self):
        '''Увеличение clock tick для данного класса'''
        self.gc += 1

    def set_animation(self, animation, callback=None, mirror_current_animation=False):
        '''Меняет тип анимации'''
        self.current_animation = animation
        self.mirror_current_animation = mirror_current_animation
        self.frame_idx = 0
        self.callback = callback
        self.gc = 0

    def start_animation_chain(self, animation_chain):
        '''Фунция для запуска цепочки анимаций'''

        def generate_callback(unit, animation, callback, action=None, action_args=None, mirror_animation=False):
            '''Генерирует функцию возврата и связывает с последующим шагом'''

            def f():
                unit.set_animation(animation, callback, mirror_animation)
                if action is not None and action_args is not None:
                    action(*action_args)

            return f

        last = None
        for i in animation_chain:
            last = generate_callback(self, i.animation, last, action=i.action, action_args=i.action_args,
                                     mirror_animation=i.mirror)
        last()


class MovableAnimatedSprite(AnimatedSprite):
    '''Класс расширяющий animated sprite, добавляюший фунционал перемещения спрайта'''

    def __init__(self, animations, x, y, group, scale_to, default_animation, mirror_animation=False):
        '''Инициализация класса'''
        super().__init__(animations, x, y, group, scale_to, default_animation, mirror_animation)
        self.derired_position = None
        self.dx = 0
        self.dy = 0
        self.ax = self.rect.x
        self.ay = self.rect.y
        self.ticks_count = 0
        self.current_tick = 0

    def move(self, x, y):
        '''Функция для задания изменения позиции спрайта на экране'''
        fps_mod = self.animations[self.current_animation].fps_mod
        frames_cnt = len(self.frames[self.current_animation])
        self.ticks_count = fps_mod * frames_cnt
        self.dx = x / self.ticks_count
        self.dy = y / self.ticks_count
        self.ax = self.rect.x
        self.ay = self.rect.y
        self.current_tick = 0

    def move_tick(self):
        '''Функция для изменения шага перемещения'''
        if self.current_tick < self.ticks_count:
            self.ax += self.dx
            self.ay += self.dy
            self.rect.x = self.ax
            self.rect.y = self.ay
            self.current_tick += 1

    def set_position(self, x, y):
        '''Функция для мгновенного изменения позиции спрайта'''
        self.rect.x = x
        self.rect.y = y
