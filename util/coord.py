from __future__ import annotations

import math

import pygame

from consts import BOARD_OFFSET, TILE_SIZE


def translate_coords(x, y, degrees, distance):
	rads = math.radians(degrees)
	delta_x = distance * math.cos(rads)
	delta_y = distance * math.sin(rads)
	x_new = x + delta_x
	y_new = y + delta_y
	return x_new, y_new


def get_rect_in_grid(x, y, size_x, size_y):
	# rect = pygame.Rect((x - (size_x/TILE_SIZE - 1) / 2) * TILE_SIZE + BOARD_OFFSET[0],
	# 				   (y - (size_y/TILE_SIZE - 1) / 2) * TILE_SIZE + BOARD_OFFSET[1], size_x, size_y)
	tx = -0.5 * size_x + (x + 0.5) * TILE_SIZE + BOARD_OFFSET[0]
	ty = -0.5 * size_y + (y + 0.5) * TILE_SIZE + BOARD_OFFSET[1]
	rect = pygame.Rect(tx, ty, size_x, size_y)
	return rect
