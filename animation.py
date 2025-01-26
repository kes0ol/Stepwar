import pygame


class AnimationParams:
    def __init__(self, sheet, columns, rows, w, h, ltop_x, ltop_y, fps_mod):
        self.sheet = sheet
        self.columns = columns
        self.rows = rows
        self.w, self.h = w, h
        self.ltop_x, self.ltop_y = ltop_x, ltop_y
        self.fps_mod = fps_mod


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
        self.callback = None
        self.gc = 0

    def cut_sheet(self, sheet, columns, rows, w, h, ltop_x, ltop_y):
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (ltop_x + w * i, ltop_y + h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, (w, h)))

                image = pygame.transform.scale(image, (self.scale_to, self.scale_to))
                frames.append(image)
        return frames

    def next(self):
        if self.gc % self.animations[self.current_animation].fps_mod == 0:
            self.frame_idx += 1
            if self.frame_idx == len(self.frames[self.current_animation]) and self.callback is not None:
                self.callback(self)
            self.frame_idx %= len(self.frames[self.current_animation])
            self.image = self.frames[self.current_animation][self.frame_idx]
        self.gc += 1

    def set_animation(self, animation, callback=None):
        self.current_animation = animation
        self.callback = callback
