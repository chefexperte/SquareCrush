import random

from pygame_imp.game import PgGame
from universal.consts import TILE_SIZE, WINDOW_WIDTH
from game_math.coord import translate_coords
from tile import Tile
from pygame_imp.ui_object import PgUILabel
from pygame_imp.visual.animation import PgTileAnimation, PgAnimation


def play_block_break(game: PgGame, color: tuple[int, int, int], pos: tuple[int, int]):
	anims: list[PgTileAnimation] = create_explosion_effect(game, color, pos)
	for i in range(len(anims)):
		anim = anims[i]
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -110 / TILE_SIZE, 0, 0.1)
		dist = -game.ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - anim.end[1])))
		finish = PgTileAnimation(anim.tile, anim.end, score_pos, "lin", game.ANIMATION_SPEED * 2 + dist)
		if i < 2:
			finish.on_finish = lambda: game.add_score(1)
		anim.on_finish = lambda a=finish: game.add_anim(a)
		game.add_anim(anim)


def create_explosion_effect(game: PgGame, color: tuple[int, int, int], pos: tuple[int, int]):
	animations: list[PgTileAnimation] = []
	particle_num = 10
	for i in range(particle_num):
		tile = Tile(color)
		start = (pos[0], pos[1], random.random() * 180 - 90, 0.2)
		end = (pos[0] + random.random() * 1.25 - 0.625, pos[1] + random.random() * 1.25 - 0.625,
			   random.random() * 180 - 90, 0.35)
		anim = PgTileAnimation(tile, start, end, "ease_out", game.EXPLOSION_SPEED * game.ANIM_SPEED_MULT)
		animations.append(anim)
	return animations


def create_circle_effect(game: PgGame, color: tuple[int, int, int], pos: tuple[float, float], size: float, particle_num: int,
						 speed: float):
	animations: list[PgTileAnimation] = []
	for i in range(particle_num):
		angle = 360 / particle_num * i
		goal = translate_coords(pos[0], pos[1], angle, size)
		start = (pos[0], pos[1], angle, 0.1)
		end = (goal[0], goal[1], angle + 360 * 2, 0.25)
		anim = PgTileAnimation(Tile(color), start, end, "ease_out", speed + (random.random() - 0.5) * 2)
		animations.append(anim)
	return animations


def play_bonus_point_effect(game: PgGame, color: tuple[int, int, int], pos: tuple[float, float], size: float, score: int):
	particle_num = 30
	score_per_particle = score // particle_num
	remainder = score % particle_num
	anims = create_circle_effect(game, color, pos, size, particle_num, game.ANIMATION_SPEED)
	for i in range(len(anims)):
		anim = anims[i]
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -110 / TILE_SIZE, 0, 0.1)
		dist = -game.ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - anim.end[1])))
		finish = PgTileAnimation(Tile(color), anim.end, score_pos, "lin", game.ANIMATION_SPEED * 2 + dist)
		if i < remainder:
			finish.on_finish = lambda: game.add_score(1 + score_per_particle)
		else:
			finish.on_finish = lambda: game.add_score(score_per_particle)
		anim.on_finish = lambda a=finish: game.add_anim(a)
		game.add_anim(anim)


def play_shout_popup_effect(game: PgGame, color: tuple[int, int, int], pos: tuple[float, float], size: float, text: str):
	# make an animation for a text popping up that motivates the player
	font = game.game_fonts.shout_font
	label = PgUILabel(text, font, color, pos)
	anim = PgAnimation(label.surface, color, (pos[0], pos[1], random.randint(-25, 25), 0.1), (pos[0], pos[1] - 1, 0, size),
					 "ease_out", game.ANIMATION_SPEED * 0.5, priority=1)
	game.add_anim(anim)
