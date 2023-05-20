from typing import Callable

import pygame

from universal.ui_object import UIObject, UILabel
from universal.wrapper import SQFont


class PgFont(pygame.font.Font, SQFont):
    pass


class PgUIObject(UIObject):
    on_hover: Callable[[bool], None]
    on_click: Callable
    hitbox: pygame.Rect
    surface: pygame.Surface
    hovering: bool = False

    def __init__(self, surface: pygame.Surface = None, hitbox: pygame.Rect = None, on_hover: Callable = None,
                 on_click: Callable = None, ident: str = None):
        UIObject.__init__(self, on_hover, on_click, ident)
        self.hitbox: pygame.Rect = hitbox
        self.surface: pygame.Surface = surface
        REGISTRY[ident] = self

    def hover(self, yes: bool):
        self.hovering = yes
        if self.on_hover:
            self.on_hover(yes)

    def click(self):
        if self.on_click:
            self.on_click()

    def draw(self, screen: pygame.Surface):
        if self.surface:
            screen.blit(self.surface, (self.hitbox[0], self.hitbox[1]))


class PgUILabel(PgUIObject, UILabel):
    font: PgFont

    def __init__(self, text: str, font: PgFont, color: tuple[int, int, int], pos: tuple[float, float],
                 on_hover: Callable = None, on_click: Callable = None, ident: str = None):
        self.font = font
        self.color = color
        self.pos = pos
        self.text = text
        self.hitbox = pygame.Rect(pos, self.surface.get_size())
        REGISTRY[ident] = self
        UILabel.__init__(self, text, font, color, pos, on_hover, on_click, ident)
        PgUIObject.__init__(self, self.surface, self.hitbox, on_hover, on_click, ident)

    def set_text(self, text: str) -> None:
        self._text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.hitbox = pygame.Rect(self.pos, self.surface.get_size())

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.center_pos())

    def center_pos(self) -> tuple[float, float]:
        return self.pos[0] - self.surface.get_width() // 2, self.pos[1] - self.surface.get_height() // 2

    text: str = property(lambda self: self._text, set_text)


REGISTRY: dict[str, PgUIObject] = {}
