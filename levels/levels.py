from typing import Callable

import game as ga
import tile
from consts import GRID_SIZE
from game import Game
from tile import Tile
from ui_object import REGISTRY


class Level:
	special_blocks: list[tuple[int, int, Tile]]
	max_steps: int
	winning_condition: Callable[[Game], bool]
	star_score: list[int]

	def __init__(self, special_blocks: list[tuple[int, int, Tile]], winning_condition: Callable[[Game], bool],
				 star_score: list[int], max_steps: int = 10):
		self.special_blocks: list[tuple[int, int, Tile]] = special_blocks
		self.star_score: list[int] = star_score
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
], lambda game: (game.score >= 100 and all_blockers_at_bottom(game)), [100, 120, 160], 15)

level_two = Level([], lambda game: (game.score > 0), [150, 250, 300], 15)
level_3 = Level([], lambda game: True, [0, 20, 50], 1)

LEVELS: list[Level] = [level_one, level_two, level_3]


def load_level(game: Game, level: Level):
	print("Loading level...")
	wl: list = [REGISTRY.get("win_label"), REGISTRY.get("win_bg_box"), REGISTRY.get("star0"), REGISTRY.get("star1"),
				REGISTRY.get("star2")]
	for w in wl:
		if w in game.ui_objects:
			game.ui_objects.remove(w)
	game.board = ga.create_board()
	game.remove_combinations()
	game.score = 0
	game.star_score = level.star_score
	game.animations.clear()
	game.steps_left = level.max_steps
	for special_block in level.special_blocks:
		game.board[special_block[0]][special_block[1]] = special_block[2]
	game.winning_condition = level.winning_condition
	game.lock_timeout = 0
	game.input_locked = False
