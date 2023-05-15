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
		x = -rect_size
		y = spacing
		counter = 0
		for level in levels.levels.LEVELS:
			counter += 1
			x += spacing + rect_size
			if x + rect_size > WINDOW_WIDTH:
				x = spacing
				y += spacing + rect_size
			rect = Rect(x, y, rect_size, rect_size)
			button = Button(str(counter), game_fonts.title_font, rect, self.game.screen)
			button.on_click = lambda level=level: (self.game.set_state(GameState.IN_GAME), levels.levels.load_level(self.game, level))
			self.buttons.append(button)

	def draw_level_selection(self):
		self.game.screen.fill((0, 0, 0))
		for button in self.buttons:
			hover = False
			if button.rect.collidepoint(self.game.mouse_pos):
				hover = True
			button.draw(hover)
		pygame.display.flip()


def level_selection_events(event, game: Game, level_sel: LevelSelection):
	if event.type == pygame.MOUSEBUTTONDOWN:
		if event.button == 1:  # Left mouse button
			for button in level_sel.buttons:
				if button.rect.collidepoint(game.mouse_pos):
					button.on_click()
