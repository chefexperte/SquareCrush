import enum
import random
from typing import Callable

from pygame import Surface

from tile import Tile, COLORS
from ui_object import UIObject
from visual.animation import Animation

GRID_SIZE = 9
TILE_SIZE = 64
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE + 150
BOARD_OFFSET = (0, 150)


def create_board():
	return [[Tile(random.choice(COLORS)) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


class GameState(enum.Enum):
	MAIN_MENU = 0
	LEVEL_SELECTION = 1
	IN_GAME = 2
	PAUSE_MENU = 3


class Game:
	first_tile = None
	board = create_board()
	no_draw: set[tuple] = set()
	animations: list[Animation]
	FPS = 120
	score = 0
	steps_left = 0
	input_locked: bool = False
	lock_timeout: int = 0
	current_state = GameState.MAIN_MENU
	screen: Surface
	mouse_pos: tuple[float, float]
	chain_size: int = 0
	ui_objects: list[UIObject]

	def __init__(self):
		self.animations: list[Animation] = []
		self.ui_objects: list[UIObject] = []
		self.winning_condition: Callable[[Game], bool] = lambda game: False

	def add_score(self, score: int):
		self.score += score

	def set_state(self, state: GameState):
		self.current_state = state

	def add_anim(self, anim: Animation):
		self.animations.append(anim)

	def remove_anim(self, anim: Animation):
		if anim in self.animations:
			self.animations.remove(anim)

	def pick_random_tile(self) -> tuple[int, int]:
		# Pick a random tile. If it is None, pick a new one until it is not None
		while True:
			x = random.randint(0, GRID_SIZE - 1)
			y = random.randint(0, GRID_SIZE - 1)
			if self.board[x][y] is not None:
				return x, y

	def dec_steps(self):
		self.steps_left -= 1

	def remove_combinations(self):
		combs = self.find_combinations()
		while len(combs) > 0:
			combs = self.find_combinations()
			for comb in combs:
				self.board[comb[1][0]][comb[1][1]].color = random.choice(COLORS)

	def find_combinations(self):
		combinations = []

		# check vertical combinations
		for j in range(GRID_SIZE):
			for i in range(GRID_SIZE - 2):
				tile1: Tile = self.board[i][j]
				tile1_color = tile1.color if tile1 else None
				if ((i, j) in self.no_draw) or (tile1 is None) or not tile1.can_combine():
					continue
				comb_size = 1
				# go through each piece in the row to check for same color
				for n in range(1, GRID_SIZE - i):
					tile2 = self.board[i + n][j]
					tile2_color = tile2.color if tile2 else None
					if tile1_color == tile2_color and ((i + n, j) not in self.no_draw) and tile2.can_combine():
						comb_size += 1
					else:
						break
				# append if combination is 3 or more
				if comb_size >= 3:
					combinations.append([(k, j) for k in range(i, i + comb_size)])
					i += comb_size - 1
		# check horizontal combinations
		for i in range(GRID_SIZE):
			for j in range(GRID_SIZE - 2):
				tile1: Tile = self.board[i][j]
				tile1_color = tile1.color if tile1 else None
				if ((i, j) in self.no_draw) or (tile1 is None) or not tile1.can_combine():
					continue
				comb_size = 1
				# go through each piece in the row to check for same color
				for n in range(1, GRID_SIZE - j):
					tile2 = self.board[i][j + n]
					tile2_color = tile2.color if tile2 else None
					if tile1_color == tile2_color and ((i, j + n) not in self.no_draw) and tile2.can_combine():
						comb_size += 1
					else:
						break
				# append if combination is 3 or more
				if comb_size >= 3:
					combinations.append([(i, k) for k in range(j, j + comb_size)])
					j += comb_size - 1
		# combine combinations that match up on edges
		for combination in combinations.copy():
			for comb in combinations.copy():
				if combination == comb or comb not in combinations or combination not in combinations:
					continue
				c1f = combination[0]
				c1l = combination[-1]
				c2f = comb[0]
				c2l = comb[-1]
				if c1f == c2f or c1l == c2l or c1f == c2l or c1l == c2f:
					combinations.remove(comb)
					combinations.remove(combination)
					combinations.append(list(set(combination).union(set(comb))))
		combinations.sort(key=lambda x: len(x), reverse=True)
		return combinations
