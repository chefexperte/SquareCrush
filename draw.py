import pygame
from pygame import Surface, Rect

from game import GRID_SIZE, BOARD_OFFSET, TILE_SIZE, Game
from tile import TileAddon


def draw_rotated_rect(screen: Surface, color: tuple[int, int, int], pos: tuple[float, float], width: float,
					  height: float, angle: float, alpha: int = 255):
	# Rechteck erstellen
	rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
	try:
		pygame.draw.rect(rect_surface, (*color, alpha), (0, 0, width, height))
	except ValueError:
		print(color)

	# Rechteck um den Winkel drehen
	rotated_surface = pygame.transform.rotate(rect_surface, angle)
	rotated_rect = rotated_surface.get_rect(center=pos)

	# Rotiertes Rechteck auf dem Bildschirm anzeigen
	screen.blit(rotated_surface, rotated_rect)


def draw_board(game):
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			# if game.no_draw and (i, j) in game.no_draw:
			# 	pygame.draw.rect(screen, (150, 150, 150), (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
			if (game.no_draw and (i, j) in game.no_draw) or not game.board[i][j]:
				continue
			pygame.draw.rect(game.screen, game.board[i][j].color,
							 (i * TILE_SIZE + BOARD_OFFSET[0], j * TILE_SIZE + BOARD_OFFSET[1],
							  TILE_SIZE, TILE_SIZE), 0)
			if game.board[i][j].addon and game.board[i][j].addon == TileAddon.BLOCKER:
				draw_rotated_rect(game.screen, (0, 0, 0),
								  (
								  (i + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (j + 0.5) * TILE_SIZE + BOARD_OFFSET[1]),
								  TILE_SIZE,
								  TILE_SIZE, 0, 200)


def run_animations(game: Game):
	for anim in game.animations.copy():
		x0, y0, angle0, size0 = anim.start
		x1, y1, angle1, size1 = anim.curr
		x2, y2, angle2, size2 = anim.end
		if anim.tile:
			draw_rotated_rect(game.screen, anim.tile.color,
								  ((x1 + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (y1 + 0.5) * TILE_SIZE + BOARD_OFFSET[1]),
								  TILE_SIZE * size1, TILE_SIZE * size1, angle1)
			if anim.tile.addon == TileAddon.BLOCKER:
				draw_rotated_rect(game.screen, (0, 0, 0),
								  ((x1 + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (y1 + 0.5) * TILE_SIZE + BOARD_OFFSET[1]),
								  TILE_SIZE * size1, TILE_SIZE * size1, angle1, 200)
		# go from curr towards end
		# dx, dy = x2 - x1, y2 - y1
		# direction: tuple = dx / (dx ** 2 + dy ** 2) ** 0.5, dy / (dx ** 2 + dy ** 2) ** 0.5
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
