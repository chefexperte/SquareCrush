import pygame
from pygame import Surface, Rect


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
