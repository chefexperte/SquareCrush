import random
import warnings

import pygame
from pygame import Surface

import menu
import strings
from draw import draw_rotated_rect
from game import GRID_SIZE, TILE_SIZE, COLORS, Game, Animation, WINDOW_HEIGHT, WINDOW_WIDTH, BOARD_OFFSET, GameState
from visual.animation import FALL_SPEED, ANIMATION_SPEED
from visual.effect import play_explosion, play_bonus_point_effect
from visual.text import GameFonts


def draw_board(game):
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			# if game.no_draw and (i, j) in game.no_draw:
			# 	pygame.draw.rect(screen, (150, 150, 150), (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
			if (game.no_draw and (i, j) in game.no_draw) or not game.board[i][j]:
				continue
			pygame.draw.rect(game.screen, game.board[i][j].color,
							 (i * TILE_SIZE + BOARD_OFFSET[0], j * TILE_SIZE + BOARD_OFFSET[1],
							  TILE_SIZE, TILE_SIZE), 0)


def swap_tiles(game, pos1: tuple[int, int], pos2: tuple[int, int], animation_speed: float = None):
	board = game.board
	# add new animation
	tile1 = board[pos1[0]][pos1[1]]
	tile2 = board[pos2[0]][pos2[1]]
	game.no_draw.add(pos2)
	anim = Animation(tile1.color if tile1 else None, (pos1[0], pos1[1], 0), (pos2[0], pos2[1], 0))
	anim.on_finish = lambda: game.no_draw.remove(pos2) if pos2 in game.no_draw else print(f"tried to remove {pos2}")
	if animation_speed:
		anim.speed = animation_speed
	game.animations.append(anim)
	game.no_draw.add(pos1)
	anim2 = Animation(tile2.color if tile2 else None, (pos2[0], pos2[1], 0), (pos1[0], pos1[1], 0))
	anim2.on_finish = lambda: game.no_draw.remove(pos1) if pos1 in game.no_draw else print(f"tried to remove {pos1}")
	if animation_speed:
		anim2.speed = animation_speed
	game.animations.append(anim2)
	# swap places
	board[pos1[0]][pos1[1]], board[pos2[0]][pos2[1]] = board[pos2[0]][pos2[1]], board[pos1[0]][pos1[1]]


def remove_tile(game: Game, bl: tuple[int, int]):
	game.board[bl[0]][bl[1]] = None
	if bl in game.no_draw:
		game.no_draw.remove(bl)
	else:
		print(f"{bl} was not in no_draw")


def main(game: Game):
	remove_combinations(game)
	pygame.font.init()
	game.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption('IQ Crush')

	# init fonts
	game_fonts = GameFonts()
	main_menu = menu.MainMenu(game)
	main_menu.init(game_fonts)

	running = True
	dragging = False
	lock_timeout = True

	clock = pygame.time.Clock()

	while running:
		clock.tick(game.FPS)

		# global logic
		game.mouse_pos = pygame.mouse.get_pos()

		# state dependent logic
		if game.current_state == GameState.MAIN_MENU:
			# main menu logic
			main_menu.draw_main_menu()
		elif game.current_state == GameState.IN_GAME:
			# in game logic
			if len(game.no_draw) > 0:
				game.input_locked = True
			else:
				if game.input_locked:
					lock_timeout -= 1
					if lock_timeout == 0:
						lock_timeout = 1
						game.input_locked = False
			game.screen.fill((0, 0, 0))
			draw_board(game)
			run_animations(game)
			process_combinations(game)
			refill_tiles(game)
			game.score_label = game_fonts.title_font.render(f"{strings.IN_GAME_SCORE}{game.score}", True,
															(255, 255, 255))
			game.screen.blit(game.score_label, (WINDOW_WIDTH // 2 - game.score_label.get_width() // 2, 50))
			pygame.display.flip()

		# global event logic
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("Quitting the game")
				running = False
				break
			if game.current_state == GameState.MAIN_MENU:
				main_menu_events(event, game, main_menu)
			elif game.current_state == GameState.IN_GAME:
				if not game.input_locked:
					swap_drag(event, game)

	pygame.font.quit()


def main_menu_events(event, game: Game, main_menu: menu.MainMenu):
	if event.type == pygame.MOUSEBUTTONDOWN:
		if event.button == 1:  # Left mouse button
			for button in main_menu.buttons:
				if button.rect.collidepoint(game.mouse_pos):
					button.on_click()


def refill_tiles(game: Game):
	# refill
	refills = []
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			if (i, j) in game.no_draw or (i, j - 1) in game.no_draw:
				continue
			if not game.board[i][j] and game.board[i][j - 1]:
				if j > 0:
					refills.append(((i, j), (i, j - 1)))
	for refill in refills:
		swap_tiles(game, refill[0], refill[1], FALL_SPEED)


def process_combinations(game: Game):
	combs = find_combinations(game)
	# for comb in combs:
	if len(combs) > 0:
		comb = combs[0]
		for block in comb:
			start = (block[0] + 0.5, block[1] + 0.5, 0, 0)
			end = (block[0] + 0.5, block[1] + 0.5, 180, 0)
			anim = Animation(game.board[block[0]][block[1]].color, start, end)
			anim.on_finish = lambda bl=block: remove_tile(game, bl)
			game.no_draw.add(block)
			game.animations.append(anim)
			play_explosion(game, block)
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
			color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
			bonus = 1
			match len(comb):
				case 4:
					bonus = 2
				case 5:
					bonus = 5
			play_bonus_point_effect(game, color, (center_x, center_y), 2, len(comb) + bonus)
		if game.chain_size >= 2:
			play_bonus_point_effect(game, (60*game.chain_size, 25, 25), (center_x, center_y), 0.4 * game.chain_size, game.chain_size)


def run_animations(game: Game):
	for anim in game.animations.copy():
		x0, y0, angle0, size0 = anim.start
		x1, y1, angle1, size1 = anim.curr
		x2, y2, angle2, size2 = anim.end
		if anim.color:
			if anim.start[2] == 0 and anim.end[2] == 0:
				pygame.draw.rect(game.screen, anim.color, (
					x1 * TILE_SIZE + BOARD_OFFSET[0], y1 * TILE_SIZE + BOARD_OFFSET[1], TILE_SIZE * size1,
					TILE_SIZE * size1), 0)
			else:
				draw_rotated_rect(game.screen, anim.color,
								  (x1 * TILE_SIZE + BOARD_OFFSET[0], y1 * TILE_SIZE + BOARD_OFFSET[1]),
								  TILE_SIZE * size1, TILE_SIZE * size1, angle1)
		# go from curr towards end
		# dx, dy = x2 - x1, y2 - y1
		# direction: tuple = dx / (dx ** 2 + dy ** 2) ** 0.5, dy / (dx ** 2 + dy ** 2) ** 0.5
		x_diff_total = x2 - x0
		y_diff_total = y2 - y0
		angle_diff_total = angle2 - angle0
		size_diff_total = size2 - size0
		anim.curr = (
		x0 + x_diff_total * anim.get_anim_type_progress(), y0 + y_diff_total * anim.get_anim_type_progress(),
		angle0 + angle_diff_total * anim.get_anim_type_progress(),
		size0 + size_diff_total * anim.get_anim_type_progress())
		if anim.progress >= 1:
			if anim.on_finish:
				anim.on_finish()
			game.animations.remove(anim)
		anim.progress += 0.5 * anim.speed * (1 / game.FPS)


def find_combinations(game):
	combinations = []
	# check vertical combinations
	for j in range(GRID_SIZE):
		for i in range(GRID_SIZE - 2):
			if ((i, j) in game.no_draw) or (game.board[i][j] is None):
				continue
			tile1 = game.board[i][j]
			tile1_color = tile1.color if tile1 else None
			comb_size = 1
			# go through each piece in the row to check for same color
			for n in range(1, GRID_SIZE - i):
				tile2 = game.board[i + n][j]
				tile2_color = tile2.color if tile2 else None
				if tile1_color == tile2_color and ((i + n, j) not in game.no_draw):
					comb_size += 1
				else:
					break
			# append if combination is 3 or more
			if comb_size >= 3:
				combinations.append([(k, j) for k in range(i, i + comb_size)])
				i += comb_size - 1
	# check horizontal combinations
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE - 2):
			tile1 = game.board[i][j]
			tile1_color = tile1.color if tile1 else None
			if ((i, j) in game.no_draw) or (tile1_color is None):
				continue
			comb_size = 1
			# go through each piece in the row to check for same color
			for n in range(1, GRID_SIZE - j):
				tile2 = game.board[i][j + n]
				tile2_color = tile2.color if tile2 else None
				if tile1_color == tile2_color and ((i, j + n) not in game.no_draw):
					comb_size += 1
				else:
					break
			# append if combination is 3 or more
			if comb_size >= 3:
				combinations.append([(i, k) for k in range(j, j + comb_size)])
				j += comb_size - 1
	# combine combinations that match up on edges
	for combination in combinations.copy():
		for comb in combinations.copy():
			if combination == comb or comb not in combinations or combination not in combinations:
				continue
			c1f = combination[0]
			c1l = combination[-1]
			c2f = comb[0]
			c2l = comb[-1]
			if c1f == c2f or c1l == c2l or c1f == c2l or c1l == c2f:
				combinations.remove(comb)
				combinations.remove(combination)
				combinations.append(list(set(combination).union(set(comb))))
	combinations.sort(key=lambda x: len(x), reverse=True)
	return combinations


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
				swap_tiles(game, game.first_tile, (grid_x, grid_y))
				game.chain_size = 0
			game.first_tile = None


def remove_combinations(game: Game):
	combs = find_combinations(game)
	while len(combs) > 0:
		combs = find_combinations(game)
		for comb in combs:
			game.board[comb[1][0]][comb[1][1]].color = random.choice(COLORS)


if __name__ == "__main__":
	_game = Game()
	main(_game)
