from typing import Callable

import tile
from game import Game
from consts import GRID_SIZE
from tile import Tile
import game as ga


class Level:
	special_blocks: list[tuple[int, int, Tile]]
	max_steps: int
	winning_condition: Callable[[Game], bool]

	def __init__(self, special_blocks: list[tuple[int, int, Tile]], winning_condition: Callable[[Game], bool],
				 max_steps: int = 10):
		self.special_blocks: list[tuple[int, int, Tile]] = special_blocks
		self.max_steps: int = max_steps
		self.winning_condition: Callable[[Game], bool] = winning_condition


def all_blockers_at_bottom(game: Game) -> bool:
	for x in range(GRID_SIZE):
		for y in range(GRID_SIZE):
			t: Tile | None = game.board[x][y]
			if not t:
				continue
			if t.addon == tile.TileAddon.BLOCKER and y != GRID_SIZE - 1:
				return False
	return True


level_one = Level([
	(3, 3, Tile(tile.TileColor.PINK.value, tile.TileAddon.BLOCKER)),
	(5, 3, Tile(tile.TileColor.PINK.value, tile.TileAddon.BLOCKER))
], lambda game: (game.score >= 100 and all_blockers_at_bottom(game)), 15)

level_two = Level([], lambda game: (game.score > 0), 15)

LEVELS: list[Level] = [level_one, level_two]


def load_level(game: Game, level: Level):
	print("Loading level...")
	game.board = ga.create_board()
	game.remove_combinations()
	game.score = 0
	game.animations.clear()
	game.steps_left = level.max_steps
	for special_block in level.special_blocks:
		game.board[special_block[0]][special_block[1]] = special_block[2]
	game.winning_condition = level.winning_condition
	game.lock_timeout = 0
	game.input_locked = False
