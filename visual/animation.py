from typing import Callable

ANIMATION_SPEED = 5
EXPLOSION_SPEED = 4
FALL_SPEED = 12.5


class Animation:
	def __init__(self, color: tuple[int, int, int] = (0, 0, 0), start: tuple = (0, 0),
				 end: tuple = (0, 0), anim_type: str = "lin", speed: float = ANIMATION_SPEED):
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

	progress: float = 0
	color: tuple[int, int, int] = None
	# x, y, rot, size
	start: tuple[float, float, float, float] = None
	curr: tuple[float, float, float, float] = None
	end: tuple[float, float, float, float] = None
	anim_type: str = "lin"
	on_finish: Callable = None
	speed: float = ANIMATION_SPEED

	def get_anim_type_progress(self) -> float:
		if self.anim_type == "ease_out":
			t = self.progress - 1
			return t * t * t + 1
		if self.anim_type == "ease_in":
			t = self.progress
			return t ** 3
		return self.progress
