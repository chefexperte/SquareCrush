from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Callable

from universal.consts import TILE_SIZE, BOARD_OFFSET
from tile import Tile
from universal.wrapper import SQDrawable


def tile_to_real_pos(pos: tuple[float, float]) -> tuple[float, float]:
	return (pos[0] + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (pos[1] + 0.5) * TILE_SIZE + BOARD_OFFSET[1]


class Animation(ABC):
	def __init__(self, drawable: SQDrawable, color: tuple[int, int, int] = (255, 255, 255), start: tuple = (-1, -1),
				 end: tuple = (-1, -1), anim_type: str = "lin", speed: float = 2.5, delay: float = 0,
				 priority: int = 0):
		self.delay = delay
		self.drawable = drawable
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
	drawable: SQDrawable = None
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

	@abstractmethod
	def draw(self, drawable: SQDrawable):
		print("Animation.draw()")
		pass


class TileAnimation(Animation, ABC):
	def __init__(self, tile: Tile = Tile((0, 0, 0)), start: tuple = (-1, -1),
				 end: tuple = (-1, -1), anim_type: str = "lin", speed: float = 2.5, delay: float = 0):
		self.tile = tile
		drawable = SQDrawable()
		color = tile.color if tile else None
		if len(start) != len(end):
			raise ValueError("Start and end tuples have to be the same length")
		super().__init__(drawable, color, start, end, anim_type, speed, delay)

	tile: Tile = None

	@abstractmethod
	def draw(self, drawable: SQDrawable):
		print("TileAnimation.draw()")
		pass

