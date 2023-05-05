import random

from game import Game, WINDOW_WIDTH, TILE_SIZE
from visual.animation import Animation, EXPLOSION_SPEED, ANIMATION_SPEED


def play_explosion(game: Game, pos: tuple[int, int]):
	for i in range(10):
		color = game.board[pos[0]][pos[1]].color
		start = (pos[0] + 0.5, pos[1] + 0.5, random.random() * 180 - 90, 0.2)
		end = (pos[0] + random.random() * 1.25 - 0.125, pos[1] + random.random() * 1.25 - 0.125,
			   random.random() * 180 - 90, 0.35)
		anim = Animation(color, start, end, "lin", EXPLOSION_SPEED)
		score_pos = (WINDOW_WIDTH // 2 // TILE_SIZE, -50 // TILE_SIZE, 0, 0.1)
		dist = -ANIMATION_SPEED * 0.1 * (max(3, abs(score_pos[1] - end[1])))
		finish = Animation(color, end, score_pos, "lin", ANIMATION_SPEED * 2 + dist)
		if i < 5:
			finish.on_finish = lambda: game.add_score(1)
		anim.on_finish = lambda a=finish: game.animations.append(a)
		game.animations.append(anim)
