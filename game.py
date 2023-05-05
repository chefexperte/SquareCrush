import random

import pygame

from tile import Tile, COLORS
from visual.animation import Animation

GRID_SIZE = 8
TILE_SIZE = 64
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE + 150
BOARD_OFFSET = (0, 150)


def create_board():
	return [[Tile(random.choice(COLORS)) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


class Game:
	first_tile = None
	board = create_board()
	no_draw: set[tuple] = set()
	animations: list[Animation] = None
	title_font: pygame.font.Font = None
	score_label: pygame.surface.Surface = None
	FPS = 120
	score = 0

	def __init__(self):
		self.animations: list[Animation] = []

	def add_score(self, score: int):
		self.score += score
