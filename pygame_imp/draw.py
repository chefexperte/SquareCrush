import pygame
from pygame import Surface

from universal.consts import GRID_SIZE, TILE_SIZE, BOARD_OFFSET
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
