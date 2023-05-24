import random

from consts import TILE_SIZE, WINDOW_WIDTH
from game import Game
from util.coord import translate_coords
from tile import Tile
from ui_object import UILabel
from util.game_color import GameColor
from visual.animation import TileAnimation, Animation, AnimationCheckpoint


def play_block_break(game: Game, color: GameColor, pos: tuple[int, int]):
	anims: list[TileAnimation] = create_explosion_effect(game, color, pos)
	for i in range(len(anims)):
		anim = anims[i]
		score_pos = AnimationCheckpoint((WINDOW_WIDTH // 2 // TILE_SIZE, -110 / TILE_SIZE), color, 0, 0.1)
		dist = -game.ANIMATION_SPEED * 0.1 * (max(3., abs(score_pos.pos[1] - anim.end.pos[1])))
		finish = TileAnimation(anim.tile, anim.end, score_pos, "lin", game.ANIMATION_SPEED * 2 + dist)
		if i < 2:
			finish.on_finish = lambda: game.add_score(1)
		anim.on_finish = lambda a=finish: game.add_anim(a)
		game.add_anim(anim)


def create_explosion_effect(game: Game, color: GameColor, pos: tuple[int, int]):
	animations: list[TileAnimation] = []
	particle_num = 10
	for i in range(particle_num):
		tile = Tile(color)
		start = AnimationCheckpoint(pos, color, random.random() * 180 - 90, 0.2)
		end = AnimationCheckpoint((pos[0] + random.random() * 1.25 - 0.625, pos[1] + random.random() * 1.25 - 0.625),
								  color,
								  random.random() * 180 - 90, 0.35)
		anim = TileAnimation(tile, start, end, "ease_out", game.EXPLOSION_SPEED * game.ANIM_SPEED_MULT)
		animations.append(anim)
	return animations


def create_circle_effect(game: Game, color: GameColor, pos: tuple[float, float], size: float,
						 particle_num: int, speed: float):
	animations: list[TileAnimation] = []
	for i in range(particle_num):
		angle = 360 / particle_num * i
		goal = translate_coords(pos[0], pos[1], angle, size)
		start = AnimationCheckpoint(pos, color, angle, 0.1)
		end = AnimationCheckpoint(goal, color, angle + 360 * 2, 0.25)
		anim = TileAnimation(Tile(color), start, end, "ease_out", speed + (random.random() - 0.5) * 2)
		animations.append(anim)
	return animations


def play_bonus_point_effect(game: Game, color: GameColor, pos: tuple[float, float], size: float, score: int):
	particle_num = 30
	score_per_particle = score // particle_num
	remainder = score % particle_num
	anims = create_circle_effect(game, color, pos, size, particle_num, game.ANIMATION_SPEED)
	for i in range(len(anims)):
		anim = anims[i]
		score_pos = AnimationCheckpoint((WINDOW_WIDTH // 2 // TILE_SIZE, -110 / TILE_SIZE), color, 0, 0.1)
		dist = -game.ANIMATION_SPEED * 0.1 * (max(3., abs(score_pos.pos[1] - anim.end.pos[1])))
		finish = TileAnimation(Tile(color), anim.end, score_pos, "lin", game.ANIMATION_SPEED * 2 + dist)
		if i < remainder:
			finish.on_finish = lambda: game.add_score(1 + score_per_particle)
		else:
			finish.on_finish = lambda: game.add_score(score_per_particle)
		anim.on_finish = lambda a=finish: game.add_anim(a)
		game.add_anim(anim)


def play_shout_popup_effect(game: Game, color: GameColor, pos: tuple[float, float], size: float, text: str):
	# make an animation for a text popping up that motivates the player
	font = game.game_fonts.shout_font
	label = UILabel(text, font, color, pos)
	angle1 = random.randint(-40, 40)
	angle2 = random.randint(-20, 20)
	p1 = AnimationCheckpoint(pos, color, angle1, 0.1)
	p2 = AnimationCheckpoint(pos, color, angle2, size)
	anim = Animation(label.surface, p1, p2, "ease_out", game.ANIMATION_SPEED * 0.5, priority=1)
	game.add_anim(anim)
