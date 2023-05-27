from typing import Callable, Optional

import pygame

from util.game_color import GameColor
from util.priority_object import PriorityDrawable


class UIObject(PriorityDrawable):
	on_hover: Callable[[bool], None]
	on_click: Callable
	hitbox: pygame.Rect
	surface: pygame.Surface
	hovering: bool = False
	priority: int = 0

	def __init__(self, surface: pygame.Surface | None = None, hitbox: pygame.Rect | None = None,
				 on_hover: Callable[[bool], None] | None = None,
				 on_click: Optional[Callable] = None, ident: str | None = None, priority: int = 0):
		self.on_hover: Callable[[bool], None] = on_hover
		self.on_click: Callable = on_click
		self.hitbox: pygame.Rect = hitbox
		self.surface: pygame.Surface = surface
		self.priority = priority
		if not ident:
			ident = str(id(self))
		REGISTRY[ident] = self
		PriorityDrawable.__init__(self, priority)

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


class UILabel(UIObject):
	_text: str
	font: pygame.font.Font
	color: GameColor

	def __init__(self, text: str, font: pygame.font.Font, color: GameColor, pos: tuple[float, float],
				 on_hover: Optional[Callable] = None, on_click: Optional[Callable] = None, ident: str | None = None,
				 priority: int = 0):
		self.font = font
		self.color = color
		self.pos = pos
		self.text = text
		self.hitbox = pygame.Rect(pos, self.surface.get_size())
		UIObject.__init__(self, self.surface, self.hitbox, on_hover, on_click, ident, priority)

	def _set_text(self, text: str) -> None:
		self._text = text
		self.surface = self.font.render(self.text, True, self.color.to_tuple())
		self.hitbox = pygame.Rect(self.pos, self.surface.get_size())

	def draw(self, screen: pygame.Surface) -> None:
		screen.blit(self.surface, self.center_pos())

	def center_pos(self) -> tuple[float, float]:
		return self.pos[0] - self.surface.get_width() // 2, self.pos[1] - self.surface.get_height() // 2

	text: str = property(lambda self: self._text, _set_text)


REGISTRY: dict[str, UIObject] = {}
