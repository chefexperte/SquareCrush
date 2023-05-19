from __future__ import annotations

from typing import Callable

import pygame

import game
from consts import TILE_SIZE, BOARD_OFFSET
from draw import draw_rotated_rect
from tile import Tile, TileAddon


def tile_to_real_pos(pos: tuple[float, float]) -> tuple[float, float]:
	return (pos[0] + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (pos[1] + 0.5) * TILE_SIZE + BOARD_OFFSET[1]


class Animation:
	def __init__(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 255, 255), start: tuple = (-1, -1),
				 end: tuple = (-1, -1), anim_type: str = "lin", speed: float = 2.5, delay: float = 0,
				 priority: int = 0):
		self.delay = delay
		self.surface = surface
		self.color = color
		if len(start) != len(end):
			raise ValueError("Start and end tuples have to be the same length")
		if len(start) == 2:
			start = start + (0,)
			end = end + (0,)
		if len(start) == 3:
			start = start + (1,)
			end = end + (1,)
		self.start = start
		self.end = end
		self.curr = start
		self.anim_type = anim_type
		self.speed = speed
		self.priority = priority

	progress: float = 0
	surface: pygame.Surface = None
	color: tuple[int, int, int] = None
	# x, y, rot, size
	start: tuple[float, float, float, float] = None
	curr: tuple[float, float, float, float] = None
	end: tuple[float, float, float, float] = None
	anim_type: str = "lin"
	on_finish: Callable = None
	on_start: Callable = None
	starting_condition: Callable = None
	speed: float = 2.5
	delay: float = 0
	priority: int = 0

	def get_anim_type_progress(self) -> float:
		if self.anim_type == "ease_out":
			t = self.progress - 1
			return t * t * t + 1
		if self.anim_type == "ease_in":
			t = self.progress
			return t ** 3
		return self.progress

	def draw(self, screen: pygame.Surface):
		x0, y0, angle0, size0 = self.start
		x1, y1, angle1, size1 = self.curr
		x2, y2, angle2, size2 = self.end
		rect_surface = self.surface.copy()

		# Rechteck um den Winkel drehen
		rotated_surface = pygame.transform.rotate(rect_surface, angle1)
		rotated_rect = rotated_surface.get_rect(center=tile_to_real_pos((x1, y1)))
		rotated_rect.scale_by(size1)

		# Rotiertes Rechteck auf dem Bildschirm anzeigen
		# game.screen.blit(rotated_surface, rotated_rect)
		screen.blit(rotated_surface, rotated_rect)


class TileAnimation(Animation):
	def __init__(self, tile: Tile = Tile((0, 0, 0)), start: tuple = (-1, -1),
				 end: tuple = (-1, -1), anim_type: str = "lin", speed: float = 2.5, delay: float = 0):
		self.tile = tile
		surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
		color = tile.color if tile else None
		if len(start) != len(end):
			raise ValueError("Start and end tuples have to be the same length")
		super().__init__(surface, color, start, end, anim_type, speed, delay)

	tile: Tile = None

	def draw(self, screen: pygame.Surface):
		x0, y0, angle0, size0 = self.start
		x1, y1, angle1, size1 = self.curr
		x2, y2, angle2, size2 = self.end
		if self.tile:
			draw_rotated_rect(screen, self.tile.color, tile_to_real_pos((x1, y1)),
								  TILE_SIZE * size1, TILE_SIZE * size1, angle1)
			if self.tile.addon == TileAddon.BLOCKER:
				draw_rotated_rect(screen, (0, 0, 0), tile_to_real_pos((x1, y1)),
								  TILE_SIZE * size1, TILE_SIZE * size1, angle1, 200)

