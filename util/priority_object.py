import abc

import pygame


class PriorityDrawable(abc.ABC):
	priority: int = 0

	def __init__(self, priority: int):
		self.priority = priority

	@staticmethod
	def draw(screen: pygame.Surface):
		pass
