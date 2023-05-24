# Farben
import enum

from util.game_color import GameColor

COLORS_OLD = [
	(153, 102, 255),  # purple
	# (255, 127, 80),  # red
	(255, 215, 0),  # yellow
	(255, 182, 193),  # pink
	(84, 224, 168),  # green
	# (218, 112, 214),  # dark violet
	# (240, 230, 140),  # khaki
	# (255, 165, 0),  # dark orange
	(0, 191, 255)  # blue
]


class TileColor(enum.Enum):
	PURPLE = GameColor(153, 102, 255)
	YELLOW = GameColor(255, 215, 0)
	PINK = GameColor(255, 182, 193)
	GREEN = GameColor(84, 224, 168)
	BLUE = GameColor(0, 191, 255)


class TileAddon(enum.Enum):
	NONE = 0
	FROZEN = 1  # Cannot be moved until combined two times
	BOMB = 2  # Destroys all tiles around it
	BLOCKER = 3  # Cannot be moved or destroyed
	LOCKED = 4  # Cannot be moved


class Tile:
	addon: TileAddon

	def __init__(self, color: GameColor, addon: TileAddon = TileAddon.NONE):
		self.color: GameColor = color
		self.addon: TileAddon = addon

	def can_combine(self):
		return self.addon != TileAddon.BLOCKER

	def can_be_moved(self):
		return self.addon not in [TileAddon.BLOCKER, TileAddon.LOCKED, TileAddon.FROZEN]
