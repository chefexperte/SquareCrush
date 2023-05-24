#!/bin/python
import os
import random

import pygame

import draw
import strings
from game import Game, GameState, run_animations
from consts import GRID_SIZE, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_OFFSET
from rooms import main_menu as mm, level_selection
from rooms.level_selection import level_selection_events
from rooms.main_menu import main_menu_events
from tile import Tile, TileColor
from ui_object import UIObject, UILabel, REGISTRY
from util.game_color import GameColor, GameColors
from visual import image
from visual.animation import TileAnimation, AnimationCheckpoint
from visual.effect import play_bonus_point_effect, play_block_break, create_circle_effect, play_shout_popup_effect
from visual.text import GameFonts


def swap_tiles(game: Game, pos1: tuple[int, int], pos2: tuple[int, int], animation_speed: float | None):
	board = game.board
	# add new animation
	tile1 = board[pos1[0]][pos1[1]]
	tile2 = board[pos2[0]][pos2[1]]
	game.no_draw.add(pos2)
	if tile1:
		anim = TileAnimation(tile1, AnimationCheckpoint(pos1, tile1.color), AnimationCheckpoint(pos2, tile1.color))
	else:
		anim = TileAnimation(None, AnimationCheckpoint(pos1), AnimationCheckpoint(pos2))
	anim.on_finish = lambda: game.no_draw.remove(pos2) if pos2 in game.no_draw else print(f"tried to remove {pos2}")
	if animation_speed:
		anim.speed = animation_speed
	game.add_anim(anim)
	game.no_draw.add(pos1)
	if tile2:
		anim2 = TileAnimation(tile2, AnimationCheckpoint(pos2, tile2.color), AnimationCheckpoint(pos1, tile2.color))
	else:
		anim2 = TileAnimation(None, AnimationCheckpoint(pos2), AnimationCheckpoint(pos1))
	anim2.on_finish = lambda: game.no_draw.remove(pos1) if pos1 in game.no_draw else print(f"tried to remove {pos1}")
	if animation_speed:
		anim2.speed = animation_speed
	game.add_anim(anim2)
	# swap places
	board[pos1[0]][pos1[1]], board[pos2[0]][pos2[1]] = board[pos2[0]][pos2[1]], board[pos1[0]][pos1[1]]


def remove_tile(game: Game, bl: tuple[int, int]):
	game.board[bl[0]][bl[1]] = None
	if bl in game.no_draw:
		game.no_draw.remove(bl)
	else:
		print(f"{bl} was not in no_draw")


def draw_ingame_ui(game: Game):
	for o in game.ui_objects:
		o.draw(game.screen)
		if o.hitbox.collidepoint(game.mouse_pos):
			o.hover(True)
		else:
			o.hover(False)


def main(game: Game):
	game.remove_combinations()
	pygame.font.init()
	game.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption('Square Crush')

	# init fonts
	game.game_fonts = GameFonts()
	main_menu = mm.MainMenu(game)
	main_menu.init()
	level_sel = level_selection.LevelSelection(game)
	level_sel.init()

	arrow_back = image.load_image("arrow_back", (30, 30))
	game.ui_objects.append(UIObject(arrow_back, pygame.Rect(15, 5, 30, 30), on_click=lambda: game.end_level()))
	score_label = UILabel("SCORE", game.game_fonts.title_font, GameColor(), (WINDOW_WIDTH // 2, 80),
						  ident="score_label")
	game.ui_objects.append(score_label)
	turns_label = UILabel("TURNS", game.game_fonts.title_font, GameColor(), (WINDOW_WIDTH // 2, 55),
						  ident="turns_label")
	game.ui_objects.append(turns_label)

	running = True
	dragging = False

	clock = pygame.time.Clock()

	while running:
		clock.tick(game.FPS)

		# global logic
		game.mouse_pos = pygame.mouse.get_pos()

		# state dependent logic
		if game.current_state == GameState.MAIN_MENU:
			# main menu logic
			main_menu.draw_main_menu()
		elif game.current_state == GameState.LEVEL_SELECTION:
			# main menu logic
			level_sel.draw_level_selection()
		elif game.current_state == GameState.IN_GAME:
			# in game logic
			draw_in_game(game)

		# global event logic
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("Quitting the game")
				running = False
				break
			if game.current_state == GameState.MAIN_MENU:
				main_menu_events(event, game, main_menu)
			elif game.current_state == GameState.LEVEL_SELECTION:
				level_selection_events(event, game, level_sel)
			elif game.current_state == GameState.IN_GAME:
				in_game_events(event, game)

	pygame.font.quit()


def draw_in_game(game: Game):
	if len(game.no_draw) > 0:
		game.input_locked = True
	else:
		if game.input_locked:
			if game.lock_timeout > 0:
				game.lock_timeout -= 1
			if game.lock_timeout == 0:
				# lock_timeout = 0
				game.input_locked = False
	game.screen.fill((0, 0, 0))
	draw.draw_board(game)  # draw the board
	run_animations(game)  # update the animations
	pygame.draw.rect(game.screen, (97, 125, 117), (0, 0, WINDOW_WIDTH, 40))  # draw the top bar
	draw_ingame_ui(game)  # draw the ui
	process_combinations(game)  # remove the tiles that are in combinations
	tile_gravity(game)  # make the tiles fall down
	refill_tiles(game)  # refill the board with new tiles if the number of tiles gets too low
	check_win(game)  # check if the winning conditions are met and if so, end the level
	label: UIObject = REGISTRY.get("score_label")
	if label and type(label) == UILabel:
		label.text = f"{strings.IN_GAME_SCORE}{game.score}"
	label2: UIObject = REGISTRY.get("turns_label")
	if label2 and type(label2) == UILabel:
		label2.text = f"{strings.IN_GAME_STEPS}{game.steps_left}"
	pygame.display.flip()


def in_game_events(event: pygame.event.Event, game: Game):
	game_rect = pygame.Rect(BOARD_OFFSET[0], BOARD_OFFSET[1], WINDOW_WIDTH, WINDOW_HEIGHT)
	if not game.input_locked and game_rect.collidepoint(pygame.mouse.get_pos()):
		swap_drag(event, game)
	if not event.type == pygame.MOUSEBUTTONDOWN:
		return
	if event.button != 1:  # Left mouse button
		return
	for ui_object in game.ui_objects:
		if ui_object.hovering:
			ui_object.click()
			break


def check_win(game):
	if game.winning_condition(game) and len(game.no_draw) == 0:
		game.winning_condition = lambda g: False
		game.input_locked = True
		game.lock_timeout = False
		game.ANIM_SPEED_MULT = 2.5
		sizes = (1.5, 2.5, 3.5, 4.5)
		last: TileAnimation
		for size in sizes:
			for anim in create_circle_effect(game, GameColor(200, 25, 40), (4, 4), size, 80,
											 game.ANIMATION_SPEED / game.ANIM_SPEED_MULT):
				anim.delay = (size * 0.5 - 0.75)
				game.add_anim(anim)
				last = anim

		# destroy tiles for remaining steps
		def destroy_remaining_tile(previous: TileAnimation | None = None):
			if game.steps_left <= 0:
				return
			# game.steps_left -= 1
			pos = game.pick_random_tile()
			tile = game.board[pos[0]][pos[1]]
			dest = TileAnimation(speed=game.ANIMATION_SPEED)
			if previous is not None:
				dest.starting_condition = lambda game=game, ani=previous: (
						ani not in game.animations and len(game.no_draw) <= 1)
			else:
				dest.starting_condition = lambda game=game, ani=last: ani not in game.animations
			dest.delay = 0.2
			dest.on_start = lambda game=game, pos=pos, tile=tile: (
				game.add_score(5), game.dec_steps(), game.no_draw.add(pos),
				play_block_break(game, tile.color, pos))
			dest.on_finish = lambda game=game, pos=pos, p=dest: (destroy_remaining_tile(p), remove_tile(game, pos))
			game.add_anim(dest)

		destroy_remaining_tile()


def tile_gravity(game: Game):
	# refill
	falls = []
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			if (i, j) in game.no_draw or (i, j - 1) in game.no_draw:
				continue
			if not game.board[i][j] and game.board[i][j - 1]:
				if j > 0:
					falls.append(((i, j), (i, j - 1)))
	for refill in falls:
		swap_tiles(game, refill[0], refill[1], game.FALL_SPEED * game.ANIM_SPEED_MULT)


def refill_tiles(game: Game):
	if len(game.no_draw) > 0:
		return
	empty_tiles = 0
	for row in game.board:
		for column in row:
			if column is None:
				empty_tiles += 1
	if empty_tiles > 28:
		for i in range(GRID_SIZE):
			if game.board[i][0] is None:
				col: GameColor = random.choice(list(TileColor)).value
				anim = TileAnimation(Tile(col), AnimationCheckpoint((i, -1), col, 180, 0),
									 AnimationCheckpoint((i, 0), col, 0, 1), speed=game.ANIMATION_SPEED)
				anim.on_finish = \
					lambda i=i: game.no_draw.remove((i, 0)) if (i, 0) in game.no_draw else print(
						f"tried to remove {(i, 0)}")
				game.add_anim(anim)
				game.board[i][0] = Tile(col)
				game.no_draw.add((i, 0))


def process_combinations(game: Game):
	combs = game.find_combinations()
	# for comb in combs:
	if len(combs) > 0:
		comb = combs[0]
		for block in comb:
			tile = game.board[block[0]][block[1]]
			col = tile.color
			start = AnimationCheckpoint((block[0] + 0.5, block[1] + 0.5), col, 0, 0)
			end = AnimationCheckpoint((block[0] + 0.5, block[1] + 0.5), col, 180, 0)
			anim = TileAnimation(tile, start, end)
			anim.on_finish = lambda bl=block: remove_tile(game, bl)
			game.no_draw.add(block)
			game.add_anim(anim)
			play_block_break(game, tile.color, block)
		game.chain_size += 1
		x_total = 0
		y_total = 0
		for tile in comb:
			x_total += tile[0]
			y_total += tile[1]
		center_x = x_total / len(comb)
		center_y = y_total / len(comb)
		if len(comb) > 3:
			color = game.board[comb[0][0]][comb[0][1]].color
			color = GameColor(min(255, color.r + 50), min(255, color.g + 50), min(255, color.b + 50))
			bonus = 1
			match len(comb):
				case 4:
					bonus = 2
				case 5:
					bonus = 5
			play_bonus_point_effect(game, color, (center_x, center_y), 2, len(comb) + bonus)
		if game.chain_size >= 2:
			play_bonus_point_effect(game, GameColor(min(255, 60 * game.chain_size), 25, 25), (center_x, center_y),
									0.4 * game.chain_size,
									game.chain_size)
		if len(comb) > 3 or game.chain_size >= 2:
			text_intensity = min(9, max(0, (len(comb) - 3) * 3 + game.chain_size - 1 + random.randint(-2, 2)))
			play_shout_popup_effect(game, GameColor(255, 0, 0), (center_x, center_y), text_intensity / 5,
									strings.SHOUTOUTS[text_intensity])


def swap_drag(event, game):
	if event.type == pygame.MOUSEBUTTONDOWN:
		if event.button == 1:  # Left mouse button
			mouse_x, mouse_y = pygame.mouse.get_pos()
			mouse_x -= BOARD_OFFSET[0]
			mouse_y -= BOARD_OFFSET[1]
			grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
			game.first_tile = (grid_x, grid_y)
			dragging = True

	if event.type == pygame.MOUSEBUTTONUP:
		if event.button == 1:  # Left mouse button
			dragging = False
			if game.first_tile is not None:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				mouse_x -= BOARD_OFFSET[0]
				mouse_y -= BOARD_OFFSET[1]
				grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
				if grid_x == game.first_tile[0] and grid_y == game.first_tile[1]:
					return
				xdiff = grid_x - game.first_tile[0]
				ydiff = grid_y - game.first_tile[1]
				new_x = 0
				new_y = 0
				if abs(xdiff) > abs(ydiff):
					# horizontal
					new_x = 1 if xdiff > 0 else -1
				else:
					# vertical
					new_y = 1 if ydiff > 0 else -1
				grid_x, grid_y = game.first_tile[0] + new_x, game.first_tile[1] + new_y
				tile1: Tile = game.board[game.first_tile[0]][game.first_tile[1]]
				tile2: Tile = game.board[grid_x][grid_y]
				if (not tile1 or tile1.can_be_moved()) and (not tile2 or tile2.can_be_moved()):
					if game.steps_left > 0:
						game.steps_left -= 1
						swap_tiles(game, game.first_tile, (grid_x, grid_y), game.ANIMATION_SPEED)
				game.chain_size = 0
			game.first_tile = None


if __name__ == "__main__":
	# If I don't do this window decorations stink on Gnome :(
	os.environ['SDL_VIDEODRIVER'] = "x11"
	os.environ['GDK_BACKEND'] = "x11"
	_game = Game()
	main(_game)
