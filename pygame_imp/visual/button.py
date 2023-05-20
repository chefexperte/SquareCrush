from typing import Callable

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from pygame_imp.draw import draw_rotated_rect


class Button:
	text: str = ""
	font: Font
	rect: Rect
	screen: Surface
	label: Surface = property(lambda self: self.font.render(self.text, True, (255, 255, 255)))
	on_click: Callable

	def __init__(self, text: str, font: Font, rect: Rect, screen: Surface):
		self.text = text
		self.font = font
		self.rect = rect
		self.screen = screen

	def draw(self, hover: bool = False):
		rect = self.rect
		if hover:
			rect = rect.scale_by(1.1, 1.1)
		draw_rotated_rect(self.screen, (135, 85, 198), rect.center, rect.w, rect.h, 0)
		points = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
		pygame.draw.lines(self.screen, (185, 85, 238), True, points, 4)
		text_pos = (rect.centerx - self.label.get_width() // 2, rect.centery - self.label.get_height() // 2)
		self.screen.blit(self.label, text_pos)

	def click(self):
		if self.on_click:
			self.on_click()
