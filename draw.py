import pygame
from pygame import Surface


def draw_rotated_rect(screen: Surface, color: (int, int, int), pos: (int, int), width: float, height: float,
					  angle: float):
	# Rechteck erstellen
	rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
	pygame.draw.rect(rect_surface, color, (0, 0, width, height))

	# Rechteck um den Winkel drehen
	rotated_surface = pygame.transform.rotate(rect_surface, angle)
	rotated_rect = rotated_surface.get_rect(center=pos)

	# Rotiertes Rechteck auf dem Bildschirm anzeigen
	screen.blit(rotated_surface, rotated_rect)
