import math
import random

from game import Game, WINDOW_WIDTH, TILE_SIZE
from game_math.coord import translate_coords
from visual.animation import Animation, EXPLOSION_SPEED, ANIMATION_SPEED


def play_explosion(game: Game, pos: tuple[int, int]):
	particle_num = 10
	for i in range(particle_num):
		color = game.board[pos[0]][pos[1]].color
		start = (pos[0] + 0.5, pos[1] + 0.5, random.random() * 180 - 90, 0.2)
		end = (pos[0] + random.random() * 1.25 - 0.125, pos[1] + random.random() * 1.25 - 0.125,
			   random.random() * 180 - 90, 0.35)
		anim = Animation(color, start, end, "ease_out", EXPLOSION_SPEED)
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -75 / TILE_SIZE, 0, 0.1)
		dist = -ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - end[1])))
		finish = Animation(color, end, score_pos, "lin", ANIMATION_SPEED * 2 + dist)
		if i < 2:
			finish.on_finish = lambda: game.add_score(1)
		anim.on_finish = lambda a=finish: game.animations.append(a)
		game.animations.append(anim)


def play_bonus_point_effect(game: Game, color: tuple[int, int, int], pos: tuple[float, float], size: float, score: int):
	particle_num = 30
	score_per_particle = score // particle_num
	remainder = score % particle_num
	for i in range(particle_num):
		angle = 360 / particle_num * i
		goal = translate_coords(pos[0], pos[1], angle, size)
		start = (pos[0] + 0.5, pos[1] + 0.5, angle, 0.1)
		end = (0.5 + goal[0], 0.5 + goal[1],
			   angle + 360 * 2, 0.25)
		anim = Animation(color, start, end, "ease_out", ANIMATION_SPEED + (random.random() - 0.5) * 2)
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -60 // TILE_SIZE, 0, 0.1)
		dist = -ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - end[1])))
		finish = Animation(color, end, score_pos, "lin", ANIMATION_SPEED * 2 + dist)
		if i < remainder:
			finish.on_finish = lambda: game.add_score(1 + score_per_particle)
		else:
			finish.on_finish = lambda: game.add_score(score_per_particle)
		anim.on_finish = lambda a=finish: game.animations.append(a)
		game.animations.append(anim)
