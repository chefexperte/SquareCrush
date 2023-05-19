import pygame


class GameFonts:
	def __init__(self):
		self.title_font = pygame.font.Font(None, 36)
		self.shout_font = pygame.font.Font("assets/fonts/ZeroCool/ZeroCool.woff2", 45)
	title_font: pygame.font.Font
	shout_font: pygame.font.Font
