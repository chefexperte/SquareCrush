import pygame


class GameFonts:
	def __init__(self):
		self.title_font = pygame.font.Font(None, 36)
		self.score_label = self.title_font.render("Score: 0", True, (255, 255, 255))
	title_font = None
	score_label = None
