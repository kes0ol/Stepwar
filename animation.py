import pygame


class AnimationParams:
    def __init__(self, sheet, columns, rows, w, h, ltop_x, ltop_y, fps_mod):
        self.sheet = sheet
        self.columns = columns
        self.rows = rows
        self.w, self.h = w, h
        self.ltop_x, self.ltop_y = ltop_x, ltop_y
        self.fps_mod = fps_mod


class AnimationStep:
    def __init__(self, animation, action, action_args, mirror):
        self.animation = animation
        self.action = action
        self.action_args = action_args
        self.mirror = mirror


class AnimationChain:
    def __init__(self):
        self.steps = []

    def add_step(self, animation, action=None, action_args=None, mirror=False):
        self.steps.append(AnimationStep(animation, action, action_args, mirror))

    def __iter__(self):
        for i in reversed(self.steps):
            yield i


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animations, x, y, group, scale_to, default_animation):
        super().__init__(group)
        self.scale_to = scale_to
        self.rect = pygame.Rect(0, 0, scale_to, scale_to)
        self.rect = self.rect.move(x, y)
        self.frames = dict()
        self.animations = animations
        for k, v in animations.items():
            self.frames[k] = self.cut_sheet(v.sheet, v.columns, v.rows, v.w, v.h, v.ltop_x, v.ltop_y)
        self.current_animation = default_animation
        self.frame_idx = 0
        self.image = self.frames[self.current_animation][0]
        self.mirror_current_animation = False
        self.callback = None
        self.gc = 0

    def cut_sheet(self, sheet, columns, rows, w, h, ltop_x, ltop_y):
        frames = []
        mirror_frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (ltop_x + w * i, ltop_y + h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, (w, h)))

                image = pygame.transform.scale(image, (self.scale_to, self.scale_to))
                frames.append(image)
        return frames

    def next_frame(self):
        if self.gc % self.animations[self.current_animation].fps_mod == 0:
            self.frame_idx += 1
            if self.frame_idx == len(self.frames[self.current_animation]) and self.callback is not None:
                self.callback()
            self.frame_idx %= len(self.frames[self.current_animation])
            self.image = self.frames[self.current_animation][self.frame_idx]
            if self.mirror_current_animation:
                self.image = pygame.transform.flip(self.image, True, False)

    def gc_tick(self):
        self.gc += 1

    def set_animation(self, animation, callback=None, mirror_current_animation=False):
        self.current_animation = animation
        self.mirror_current_animation = mirror_current_animation
        self.frame_idx = 0
        self.callback = callback
        self.gc = 0

    def start_animation_chain(self, animation_chain):
        def generate_callback(unit, animation, callback, action=None, action_args=None, mirror_animation=False):
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
    def __init__(self, animations, x, y, group, scale_to, default_animation):
        super().__init__(animations, x, y, group, scale_to, default_animation)
        self.derired_position = None
        self.dx = 0
        self.dy = 0
        self.ax = self.rect.x
        self.ay = self.rect.y
        self.ticks_count = 0
        self.current_tick = 0

    def move(self, x, y):
        fps_mod = self.animations[self.current_animation].fps_mod
        frames_cnt = len(self.frames[self.current_animation])
        self.ticks_count = fps_mod * frames_cnt
        self.dx = x / self.ticks_count
        self.dy = y / self.ticks_count
        self.ax = self.rect.x
        self.ay = self.rect.y
        self.current_tick = 0

    def move_tick(self):
        if self.current_tick < self.ticks_count:
            self.ax += self.dx
            self.ay += self.dy
            self.rect.x = self.ax
            self.rect.y = self.ay
            self.current_tick += 1

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
