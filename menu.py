import pygame
from pygame import Rect

import strings
from game import WINDOW_WIDTH, Game, GameState
from visual.button import Button
from visual.text import GameFonts


class MainMenu:
	game: Game
	buttons: list[Button] = []
	new_game_button: Button

	def __init__(self, game: Game):
		self.buttons: list[Button] = []
		self.game: Game = game

	def init(self, game_fonts: GameFonts):
		rect_width = 400
		rect_height = 70
		rect_center = (WINDOW_WIDTH // 2, 50)
		rect = Rect(rect_center[0] - rect_width / 2, rect_center[1] - rect_height / 2, rect_width, rect_height)
		self.new_game_button = Button(strings.MAIN_MENU_NEW_GAME, game_fonts.title_font, rect, self.game.screen)
		self.new_game_button.on_click = lambda: self.game.set_state(GameState.IN_GAME)
		self.buttons.append(self.new_game_button)

	def draw_main_menu(self):
		self.game.screen.fill((0, 0, 0))
		hover = False
		if self.new_game_button.rect.collidepoint(self.game.mouse_pos):
			hover = True
		self.new_game_button.draw(hover)
		pygame.display.flip()
