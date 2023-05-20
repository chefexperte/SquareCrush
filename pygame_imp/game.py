from __future__ import annotations

import random
from typing import Callable

from pygame import Surface

from pygame_imp.visual import animation
from universal.consts import GRID_SIZE
from tile import Tile, COLORS
from pygame_imp.ui_object import PgUIObject
from pygame_imp.visual.text import GameFonts
from universal.game import GameState, Game


def create_board():
	return [[Tile(random.choice(COLORS)) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


class PgGame(Game):

	animations: list[animation.PgTileAnimation]
	screen: Surface
	ui_objects: list[PgUIObject]
	game_fonts: GameFonts

	def __init__(self):
		self.animations: list[animation.PgAnimation] = []
		self.ui_objects: list[PgUIObject] = []
		self.winning_condition: Callable[[PgGame], bool] = lambda game: False
		super().__init__()

	def add_anim(self, anim: animation.PgAnimation):
		self.animations.append(anim)
		self.animations.sort(key=lambda a: a.priority)

	def remove_anim(self, anim: animation.PgTileAnimation):
		if anim in self.animations:
			self.animations.remove(anim)

	def end_level(self):
		self.set_state(GameState.LEVEL_SELECTION)
		self.no_draw.clear()
		self.animations.clear()
		self.ANIM_SPEED_MULT = 1


def run_animations(game: PgGame):
	for anim in game.animations.copy():
		if anim.starting_condition and not anim.starting_condition():
			continue
		if anim.delay > 0:
			anim.delay -= (1 / game.FPS)
			continue
		if anim.progress == 0:
			if anim.on_start:
				anim.on_start()
		x0, y0, angle0, size0 = anim.start
		x1, y1, angle1, size1 = anim.curr
		x2, y2, angle2, size2 = anim.end
		anim.draw(game.screen)
		# go from curr towards end
		x_diff_total = x2 - x0
		y_diff_total = y2 - y0
		angle_diff_total = angle2 - angle0
		size_diff_total = size2 - size0
		anim.curr = (
			x0 + x_diff_total * anim.get_anim_type_progress(), y0 + y_diff_total * anim.get_anim_type_progress(),
			angle0 + angle_diff_total * anim.get_anim_type_progress(),
			size0 + size_diff_total * anim.get_anim_type_progress())
		if anim.progress >= 1:
			if anim.on_finish:
				anim.on_finish()
			game.animations.remove(anim)
		anim.progress += anim.speed * (1 / game.FPS)
