import pygame

from development.different.global_vars import FILL_TYPE_BORDER, FILL_TYPE_NONE


class RectCoord:
    @staticmethod
    def set_rect_coord(rect, x, y, coord_type):
        if coord_type == "center":
            rect.center = (x, y)
        elif coord_type == "bottomleft":
            rect.bottomleft = (x, y)
        elif coord_type == "bottomright":
            rect.bottomright = (x, y)
        elif coord_type == "midbottom":
            rect.midbottom = (x, y)
        else:
            rect.center = (x, y)


class Button(RectCoord):
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

    def render(self, sc):
        if self.fill_type == FILL_TYPE_BORDER:
            x, y = self.rect.center
            w = h = self.size_font
            pygame.draw.rect(sc, self.color, (x - w / 2, y - h / 2, w, h), 1)
        sc.blit(self.surfaces[self.check_click(pygame.mouse.get_pos())], self.rect)

    def check_click(self, mouse_pos):
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
