import pygame
from pygame import Surface


class GameFonts:
	def __init__(self):
		self.title_font = pygame.font.Font(None, 36)
		self.score_label = self.title_font.render("Score: 0", True, (255, 255, 255))
	title_font: pygame.font.Font
	score_label: Surface
