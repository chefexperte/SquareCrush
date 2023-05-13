import math
import random

from game import Game, WINDOW_WIDTH, TILE_SIZE
from game_math.coord import translate_coords
from tile import Tile
from visual.animation import Animation, EXPLOSION_SPEED, ANIMATION_SPEED


def play_block_break(game: Game, pos: tuple[int, int]):
	anims: list[Animation] = create_explosion_effect(game, pos)
	for i in range(len(anims)):
		anim = anims[i]
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -110 / TILE_SIZE, 0, 0.1)
		dist = -ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - anim.end[1])))
		finish = Animation(anim.tile, anim.end, score_pos, "lin", ANIMATION_SPEED * 2 + dist)
		if i < 2:
			finish.on_finish = lambda: game.add_score(1)
		anim.on_finish = lambda a=finish: game.animations.append(a)
		game.animations.append(anim)


def create_explosion_effect(game: Game, pos: tuple[int, int]):
	animations: list[Animation] = []
	particle_num = 10
	for i in range(particle_num):
		tile = game.board[pos[0]][pos[1]]
		start = (pos[0], pos[1], random.random() * 180 - 90, 0.2)
		end = (pos[0] + random.random() * 1.25 - 0.625, pos[1] + random.random() * 1.25 - 0.625,
			   random.random() * 180 - 90, 0.35)
		anim = Animation(tile, start, end, "ease_out", EXPLOSION_SPEED)
		animations.append(anim)
	return animations


def create_circle_effect(color: tuple[int, int, int], pos: tuple[float, float], size: float, particle_num: int,
						 speed: float = ANIMATION_SPEED):
	animations: list[Animation] = []
	for i in range(particle_num):
		angle = 360 / particle_num * i
		goal = translate_coords(pos[0], pos[1], angle, size)
		start = (pos[0], pos[1], angle, 0.1)
		end = (goal[0], goal[1], angle + 360 * 2, 0.25)
		anim = Animation(Tile(color), start, end, "ease_out", speed + (random.random() - 0.5) * 2)
		animations.append(anim)
	return animations


def play_bonus_point_effect(game: Game, color: tuple[int, int, int], pos: tuple[float, float], size: float, score: int):
	particle_num = 30
	score_per_particle = score // particle_num
	remainder = score % particle_num
	anims = create_circle_effect(color, pos, size, particle_num)
	for i in range(len(anims)):
		anim = anims[i]
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -110 / TILE_SIZE, 0, 0.1)
		dist = -ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - anim.end[1])))
		finish = Animation(Tile(color), anim.end, score_pos, "lin", ANIMATION_SPEED * 2 + dist)
		if i < remainder:
			finish.on_finish = lambda: game.add_score(1 + score_per_particle)
		else:
			finish.on_finish = lambda: game.add_score(score_per_particle)
		anim.on_finish = lambda a=finish: game.animations.append(a)
		game.animations.append(anim)
