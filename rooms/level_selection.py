import pygame
from pygame import Rect

import levels.levels
from game import WINDOW_WIDTH, Game, GameState
from visual.button import Button
from visual.text import GameFonts


class LevelSelection:
	game: Game
	buttons: list[Button] = []

	def __init__(self, game: Game):
		self.buttons: list[Button] = []
		self.game: Game = game

	def init(self, game_fonts: GameFonts):
		spacing = 25
		rect_size = 50
		x = 0
		y = spacing
		counter = 0
		for level in levels.levels.LEVELS:
			counter += 1
			x += spacing
			if x + rect_size > WINDOW_WIDTH:
				x = spacing
				y += spacing + rect_size
			rect = Rect(x, y, rect_size, rect_size)
			button = Button(str(counter), game_fonts.title_font, rect, self.game.screen)
			button.on_click = lambda: (self.game.set_state(GameState.IN_GAME), levels.levels.load_level(level))
			self.buttons.append(button)

	def draw_level_selection(self):
		self.game.screen.fill((0, 0, 0))
		for button in self.buttons:
			hover = False
			if button.rect.collidepoint(self.game.mouse_pos):
				hover = True
			button.draw(hover)
		pygame.display.flip()
