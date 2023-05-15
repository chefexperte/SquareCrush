from typing import Callable

import pygame


class UIObject:

	on_hover: Callable[[bool], None]
	on_click: Callable
	hitbox: pygame.Rect
	surface: pygame.Surface
	hovering: bool = False

	def __init__(self, surface: pygame.Surface = None, hitbox: pygame.Rect = None, on_hover: Callable = None,
				 on_click: Callable = None):
		self.on_hover: Callable[[bool], None] = on_hover
		self.on_click: Callable = on_click
		self.hitbox: pygame.Rect = hitbox
		self.surface: pygame.Surface = surface

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
