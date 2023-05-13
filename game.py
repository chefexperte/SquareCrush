import enum
import random
from typing import Callable

import pygame
from pygame import Surface

from tile import Tile, COLORS
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
	input_locked = False
	current_state = GameState.MAIN_MENU
	screen: Surface
	mouse_pos: tuple[float, float]
	chain_size: int = 0

	def __init__(self):
		self.animations: list[Animation] = []
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
