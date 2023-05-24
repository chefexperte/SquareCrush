from __future__ import annotations

import enum
import random
from typing import Callable

from pygame import Surface

from visual import animation
from consts import GRID_SIZE
from tile import Tile, TileColor
from ui_object import UIObject
from visual.animation import AnimationCheckpoint
from visual.text import GameFonts


def create_board() -> list[list[Tile | None]]:
	return [[Tile(random.choice(list(TileColor)).value) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


class GameState(enum.Enum):
	MAIN_MENU = 0
	LEVEL_SELECTION = 1
	IN_GAME = 2
	PAUSE_MENU = 3


class Game:

	def set_animation_speed(self, speed: float) -> None:
		self._ANIMATION_SPEED = speed

	_ANIMATION_SPEED: float = 2.5
	ANIM_SPEED_MULT: float = 1
	EXPLOSION_SPEED: float = 2
	FALL_SPEED: float = 6.25
	ANIMATION_SPEED: float = property(lambda self: self._ANIMATION_SPEED * self.ANIM_SPEED_MULT, set_animation_speed)

	first_tile: tuple[int, int] | None = None
	board: list[list[Tile | None]] = create_board()
	no_draw: set[tuple] = set()
	animations: list[animation.TileAnimation]
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
	game_fonts: GameFonts

	def __init__(self):
		self.animations: list[animation.Animation] = []
		self.ui_objects: list[UIObject] = []
		self.winning_condition: Callable[[Game], bool] = lambda game: False

	def add_score(self, score: int):
		self.score += score

	def set_state(self, state: GameState):
		self.current_state = state

	def add_anim(self, anim: animation.Animation):
		self.animations.append(anim)
		self.animations.sort(key=lambda a: a.priority)

	def remove_anim(self, anim: animation.TileAnimation):
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
				self.board[comb[1][0]][comb[1][1]].color = random.choice(list(TileColor)).value

	def find_combinations(self) -> list[list[tuple[int, int]]]:
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
					if tile1_color == tile2_color and ((i, j + n) not in self.no_draw) and tile2 and tile2.can_combine():
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

	def end_level(self):
		self.set_state(GameState.LEVEL_SELECTION)
		self.no_draw.clear()
		self.animations.clear()
		self.ANIM_SPEED_MULT = 1


def run_animations(game: Game):
	for anim in game.animations.copy():
		if anim.starting_condition and not anim.starting_condition():
			continue
		if anim.delay > 0:
			anim.delay -= (1 / game.FPS)
			continue
		if anim.progress == 0:
			if anim.on_start:
				anim.on_start()
		x0, y0, angle0, size0 = anim.start.pos[0], anim.start.pos[1], anim.start.angle, anim.start.size
		x2, y2, angle2, size2 = anim.end.pos[0], anim.end.pos[1], anim.end.angle, anim.end.size
		anim.draw(game.screen)
		# go from curr towards end
		x_diff_total = x2 - x0
		y_diff_total = y2 - y0
		angle_diff_total = angle2 - angle0
		size_diff_total = size2 - size0
		# subtract the tuples to get the difference between the two points
		new_col = anim.start.color
		anim.curr = AnimationCheckpoint(
			(x0 + x_diff_total * anim.get_anim_type_progress(), y0 + y_diff_total * anim.get_anim_type_progress()),
			new_col,
			angle0 + angle_diff_total * anim.get_anim_type_progress(),
			size0 + size_diff_total * anim.get_anim_type_progress())
		if anim.progress >= 1:
			if anim.on_finish:
				anim.on_finish()
			game.animations.remove(anim)
		anim.progress += anim.speed * (1 / game.FPS)
