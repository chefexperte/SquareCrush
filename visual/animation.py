from __future__ import annotations

from typing import Callable

import pygame

from consts import TILE_SIZE, BOARD_OFFSET
from draw import draw_rotated_rect
from util.game_color import GameColor, GameColors
from tile import Tile, TileAddon


def tile_to_real_pos(pos: tuple[float, float]) -> tuple[float, float]:
	return (pos[0] + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (pos[1] + 0.5) * TILE_SIZE + BOARD_OFFSET[1]


class AnimationCheckpoint:
	pos: tuple[float, float]
	angle: float
	size: float
	color: GameColor

	def __init__(self, pos: tuple[float, float], color: GameColor = GameColor(), angle: float = 0,
				 size: float = 1):
		self.pos = pos
		self.angle = angle
		self.size = size
		self.color = color


class Animation:
	def __init__(self, surface: pygame.Surface,
				 start: AnimationCheckpoint = AnimationCheckpoint((0, 0), GameColors.INV),
				 end: AnimationCheckpoint = AnimationCheckpoint((0, 0), GameColors.INV), anim_type: str = "lin",
				 speed: float = 2.5, delay: float = 0,
				 priority: int = 0):
		self.delay = delay
		self.surface = surface
		self.start = start
		self.end = end
		self.curr = start
		self.anim_type = anim_type
		self.speed = speed
		self.priority = priority

	progress: float = 0
	surface: pygame.Surface = None
	start: AnimationCheckpoint = None
	curr: AnimationCheckpoint = None
	end: AnimationCheckpoint = None
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
		pos, angle1, size1 = self.curr.pos, self.curr.angle, self.curr.size
		rect_surface = self.surface.copy()

		# Rechteck um den Winkel drehen
		rotated_surface = pygame.transform.rotate(rect_surface, angle1)
		rotated_rect = rotated_surface.get_rect(center=tile_to_real_pos(pos))
		rotated_rect.scale_by(size1, size1)

		# Rotiertes Rechteck auf dem Bildschirm anzeigen
		# game.screen.blit(rotated_surface, rotated_rect)
		screen.blit(rotated_surface, rotated_rect)


class TileAnimation(Animation):
	def __init__(self, tile: Tile | None = Tile(GameColor()),
				 start: AnimationCheckpoint = AnimationCheckpoint((0, 0), GameColors.INV),
				 end: AnimationCheckpoint = AnimationCheckpoint((0, 0), GameColors.INV), anim_type: str = "lin",
				 speed: float = 2.5, delay: float = 0):
		self.tile = tile
		surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
		# color = tile.color if tile else None
		super().__init__(surface, start, end, anim_type, speed, delay)

	tile: Tile = None

	def draw(self, screen: pygame.Surface):
		size = self.curr.size
		if self.tile:
			draw_rotated_rect(screen, self.curr.color, tile_to_real_pos(self.curr.pos),
							  TILE_SIZE * size, TILE_SIZE * size, self.curr.angle)
			if self.tile.addon == TileAddon.BLOCKER:
				draw_rotated_rect(screen, GameColor(0, 0, 0, 150), tile_to_real_pos(self.curr.pos),
								  TILE_SIZE * size, TILE_SIZE * size, self.curr.angle)
