import pygame

from internal.different.global_vars import FILL_TYPE_BORDER, FILL_TYPE_NONE


class RectCoord: # вспомогательный класс для работы с координатами экрана
    @staticmethod
    def set_rect_coord(rect, x, y, coord_type):
        if coord_type == "center":
            rect.center = (x, y)
        elif coord_type == "bottomleft":
            rect.bottomleft = (x, y)
        elif coord_type == "topleft":
            rect.topleft = (x, y)
        elif coord_type == "bottomright":
            rect.bottomright = (x, y)
        elif coord_type == "midbottom":
            rect.midbottom = (x, y)
        else:
            rect.center = (x, y)


class Button(RectCoord): # класс для кнопок
    def __init__(self, text, font_size, x, y, color=(0, 200, 0), dark_color=(0, 150, 0), fill_type=FILL_TYPE_NONE,
                 coord_type="center"):
        self.size_font = font_size
        self.font = pygame.font.Font(None, font_size)
        self.surfaces = [self.font.render(text, True, color), self.font.render(text, True, dark_color)]
        self.color = color
        self.dark_color = dark_color
        self.x = x
        self.y = y
        self.fill_type = fill_type
        self.rect = pygame.Rect(0, 0, *self.surfaces[0].get_rect().size)
        self.set_rect_coord(self.rect, x, y, coord_type)
        self.is_enabled = True

    def set_enabled(self, is_enabled):
        self.is_enabled = is_enabled

    def render(self, sc): # отрисовка
        if not self.is_enabled:
            return
        if self.fill_type == FILL_TYPE_BORDER:
            x, y = self.rect.center
            w = h = self.size_font
            pygame.draw.rect(sc, self.color, (x - w / 2, y - h / 2, w, h), 1)
        sc.blit(self.surfaces[self.check_click(pygame.mouse.get_pos())], self.rect)

    def check_click(self, mouse_pos): #нажатие
        if not self.is_enabled:
            return False
        return self.rect.collidepoint(mouse_pos)


class View(RectCoord):
    def __init__(self, text, font_size, x, y, color=(0, 200, 0), coord_type="center"):
        self.font = pygame.font.Font(None, font_size)
        self.x = x
        self.y = y
        self.color = color
        self.coord_type = coord_type
        self.set_text(text)

    def set_text(self, text):
        self.surface = self.font.render(text, True, self.color)
        self.rect = pygame.Rect(0, 0, *self.surface.get_rect().size)
        self.set_rect_coord(self.rect, self.x, self.y, self.coord_type)

    def render(self, sc):
        sc.blit(self.surface, self.rect)


class Edit(RectCoord):
    def __init__(self, text, font_size, x, y, w, h, color=(0, 200, 0), coord_type="center", fps_mod=20):
        self.fps_mod = fps_mod
        self.cursor_show = False
        self.cursor_pos = 0
        self.edit_started = False
        self.gc = 0
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.coord_type = coord_type
        self.text = text
        self.text_limit = 30
        self.cursor_pos = len(text)

    def render(self, sc):
        if self.edit_started:
            if self.cursor_show:
                text = self.text[:self.cursor_pos] + "|" + self.text[self.cursor_pos:]
            else:
                text = self.text[:self.cursor_pos] + " " + self.text[self.cursor_pos:]
        else:
            text = self.text
        surface = self.font.render(text, True, self.color)
        rect = pygame.Rect(0, 0, *surface.get_rect().size)
        self.set_rect_coord(rect, self.x, self.y, self.coord_type)
        sc.blit(surface, rect)

        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.set_rect_coord(self.rect, self.x, self.y, self.coord_type)
        pygame.draw.rect(sc, self.color, self.rect, 1)

    def update(self):
        if self.edit_started and self.gc % self.fps_mod == 0:
            self.cursor_show ^= 1
        self.gc += 1

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if self.edit_started:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.cursor_show = False
                    self.edit_started = False
                if event.key == pygame.K_LEFT:
                    self.cursor_pos = max([0, self.cursor_pos - 1])
                if event.key == pygame.K_RIGHT:
                    self.cursor_pos = min([len(self.text), self.cursor_pos + 1])
                if event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                if pygame.K_0 <= event.key <= pygame.K_9 and len(self.text) <= self.text_limit:
                    self.text = self.text[:self.cursor_pos] + chr(event.key) + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                if pygame.K_a <= event.key <= pygame.K_z and len(self.text) <= self.text_limit:
                    letter = event.key
                    if event.mod & pygame.KMOD_SHIFT:
                        letter -= 32
                    self.text = self.text[:self.cursor_pos] + chr(letter) + self.text[self.cursor_pos:]
                    self.cursor_pos += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.edit_started ^= self.check_click(event.pos)

    def start(self, window):
        fps = 60
        clock = pygame.time.Clock()

        self.edit_started = True
        while self.edit_started:
            for event in pygame.event.get():
                self.handle_event(event)

            window.render()
            self.update()

            clock.tick(fps)
            pygame.display.flip()
