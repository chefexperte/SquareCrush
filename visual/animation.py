from __future__ import annotations

from typing import Callable, Optional

import pygame

from consts import TILE_SIZE, BOARD_OFFSET
from draw import draw_rotated_rect
from tile import Tile, TileAddon
from util.game_color import GameColor


def tile_to_real_pos(pos: tuple[float, float]) -> tuple[float, float]:
	return (pos[0] + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (pos[1] + 0.5) * TILE_SIZE + BOARD_OFFSET[1]


class AnimationCheckpoint:
	pos: tuple[float, float]
	angle: float
	size: float
	color: GameColor

	def __init__(self, pos: tuple[float, float], color: GameColor = GameColor(a=0), angle: float = 0,
				 size: float = 1):
		self.pos = pos
		self.angle = angle
		self.size = size
		self.color = color


class Animation:
	def __init__(self, surface: pygame.Surface,
				 path: dict[float, AnimationCheckpoint] | None = None, anim_type: str = "lin",
				 speed: float = 2.5, delay: float = 0,
				 priority: int = 0):
		self.delay = delay
		self.surface = surface
		if path is None:
			path = {0: AnimationCheckpoint((0, 0)), 1: AnimationCheckpoint((0, 0))}
		else:
			if path.get(0) is None:
				raise ValueError("Animation path must contain a checkpoint at 0")
			if path.get(1) is None:
				raise ValueError("Animation path must contain a checkpoint at 1")
		if sorted(list(path.keys())) != list(path.keys()):
			print(list(path.keys()))
			print(list(path.keys()).sort())
			raise ValueError("Animation path must be sorted by time")
		self.path = path
		self.curr = path[0]
		self.anim_type = anim_type
		self.speed = speed
		self.priority = priority

	progress: float = 0
	surface: pygame.Surface = None
	curr: AnimationCheckpoint = None
	path: dict[float, AnimationCheckpoint] = None
	anim_type: str = "lin"
	on_finish: Optional[Callable] = None
	on_start: Optional[Callable] = None
	starting_condition: Optional[Callable] = None
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
		return min(1., self.progress)

	def update(self, progress: float):
		if progress == 0:
			self.curr = self.path[0]
			return
		if progress == 1:
			self.curr = self.path[1]
			return
		previous_checkpoint: tuple[float, AnimationCheckpoint] = 0, self.path[0]
		next_checkpoint: tuple[float, AnimationCheckpoint] = 1, self.path[1]
		for time, checkpoint in self.path.items():
			if time <= progress:
				previous_checkpoint = time, checkpoint
			else:
				next_checkpoint = time, checkpoint
				break
		prog_diff: float = next_checkpoint[0] - previous_checkpoint[0]
		if prog_diff != 0:
			prog = (progress - previous_checkpoint[0]) / prog_diff
		else:
			prog = 0
		new_pos = previous_checkpoint[1].pos[0] + (next_checkpoint[1].pos[0] - previous_checkpoint[1].pos[0]) * prog, \
			previous_checkpoint[1].pos[1] + (next_checkpoint[1].pos[1] - previous_checkpoint[1].pos[1]) * prog
		self.curr = AnimationCheckpoint(
			new_pos,
			previous_checkpoint[1].color.interpolate(next_checkpoint[1].color, prog),
			previous_checkpoint[1].angle + (next_checkpoint[1].angle - previous_checkpoint[1].angle) * prog,
			previous_checkpoint[1].size + (next_checkpoint[1].size - previous_checkpoint[1].size) * prog,
		)

	def draw(self, screen: pygame.Surface):
		pos, angle1, size1, col = self.curr.pos, self.curr.angle, self.curr.size, self.curr.color
		rect_surface = self.surface.copy()
		rect_surface.set_colorkey((0, 0, 0, 0))
		rect_surface.fill(col.to_tuple(), special_flags=pygame.BLEND_RGBA_MULT)

		# Rotate and scale the surface
		rotated_surface = pygame.transform.rotate(rect_surface, angle1)
		scaled_surface = pygame.transform.scale_by(rotated_surface, size1)
		rotated_rect = scaled_surface.get_rect(center=tile_to_real_pos(pos))
		rotated_rect.scale_by(size1, size1)

		# Draw the surface
		screen.blit(scaled_surface, rotated_rect)


class TileAnimation(Animation):
	def __init__(self, tile: Tile | None = Tile(GameColor()),
				 path: dict[float, AnimationCheckpoint] | None = None, anim_type: str = "lin",
				 speed: float = 2.5, delay: float = 0):
		self.tile = tile
		surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
		super().__init__(surface, path, anim_type, speed, delay)

	tile: Tile = None

	def draw(self, screen: pygame.Surface):
		size = self.curr.size
		if self.tile:
			draw_rotated_rect(screen, self.curr.color, tile_to_real_pos(self.curr.pos),
							  TILE_SIZE * size, TILE_SIZE * size, self.curr.angle)
			if self.tile.addon == TileAddon.BLOCKER:
				draw_rotated_rect(screen, GameColor(0, 0, 0, 150), tile_to_real_pos(self.curr.pos),
								  TILE_SIZE * size, TILE_SIZE * size, self.curr.angle)
