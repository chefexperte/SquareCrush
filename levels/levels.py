import game
import tile
from tile import Tile


class Level:
	SPECIAL_BLOCKS: list[tuple[int, int, Tile]] = None

	def __init__(self, special_blocks: list[tuple[int, int, Tile]]):
		self.special_blocks: list[tuple[int, int, Tile]] = special_blocks


level_one = Level([(3, 3, Tile(tile.TileColor.PINK.value, tile.TileAddon.BLOCKER))])
LEVELS: list[Level] = [level_one]


def load_level(level: Level):
	print("Loading level...")
	for special_block in level.special_blocks:
		game.Game.board[special_block[0]][special_block[1]] = special_block[2]
