from __future__ import annotations


class GameColor:

	def __init__(self, r=255, g=255, b=255, a=255):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def to_tuple(self):
		return self.r, self.g, self.b, self.a

	def interpolate(self, other: GameColor, percent: float):
		i_r = int(self.r + (other.r - self.r) * percent)
		i_g = int(self.g + (other.g - self.g) * percent)
		i_b = int(self.b + (other.b - self.b) * percent)
		i_a = int(self.a + (other.a - self.a) * percent)
		return GameColor(i_r, i_g, i_b, i_a)

	def __iter__(self):
		return iter([self.r, self.g, self.b, self.a])

	def __repr__(self):
		return f"GameColor({self.r}, {self.g}, {self.b}, {self.a})"

	def __str__(self):
		return f"GameColor({self.r}, {self.g}, {self.b}, {self.a})"

	def __eq__(self, other):
		if other is None:
			return False
		return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

	def __ne__(self, other):
		return not self.__eq__(other)


class GameColors:
	INV: GameColor = GameColor(0, 0, 0, 0)
	BLACK: GameColor = GameColor(0, 0, 0, 255)
	WHITE: GameColor = GameColor(255, 255, 255, 255)
