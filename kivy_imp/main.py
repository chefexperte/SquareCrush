import random

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.widget import Widget

from tile import Tile
from universal.game import Game

WINDOW_WIDTH = 900 * 0.55
WINDOW_HEIGHT = 1600 * 0.55
GRID_SIZE_X = 8
GRID_SIZE_Y = 9
TILE_SIZE = WINDOW_WIDTH / GRID_SIZE_X


def scale_color(color: tuple[float, float, float]) -> tuple[float, float, float]:
    return color[0] / 255, color[1] / 255, color[2] / 255


class SQTile(Widget):

    def get_color(self):
        return scale_color(self.tile.color)

    def set_color(self, color: tuple[float, float, float]):
        self.tile.color = color

    color: tuple[float, float, float] = property(get_color, set_color)

    def __init__(self, tile: Tile, pos: tuple[float, float], **kwargs):
        super(SQTile, self).__init__(**kwargs)
        self.tile: Tile = tile

        with self.canvas:
            Color(*self.color, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.size = (TILE_SIZE, TILE_SIZE)
            self.pos = pos
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.rect.size = self.size

    def on_pos(self, *args):
        self.rect.pos = self.pos


class SquareCrush(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = Game()
        self.game.steps_left = 100
        self.grid: list[list[SQTile | None]] = [[None for _ in range(GRID_SIZE_Y)] for _ in range(GRID_SIZE_X)]

        for i in range(GRID_SIZE_X):
            for j in range(GRID_SIZE_Y):
                tile: Tile = self.game.board[i][j]
                sqt = SQTile(tile, (i * TILE_SIZE, j * TILE_SIZE))
                self.grid[i][j] = sqt
                self.add_widget(sqt)

    def on_touch_down(self, touch: MouseMotionEvent):
        print(touch.button)
        if touch.button == 'left' or platform == 'android':
            # old code
            mouse_x, mouse_y = touch.pos
            grid_x, grid_y = int(mouse_x // TILE_SIZE), int(mouse_y // TILE_SIZE)
            self.game.first_tile = (grid_x, grid_y)
            dragging = True

    def on_touch_up(self, touch: MouseMotionEvent):
        if touch.button == 'left' or platform == 'android':
            # old code
            if self.game.first_tile is not None:
                mouse_x, mouse_y = touch.pos
                grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                if grid_x == self.game.first_tile[0] and grid_y == self.game.first_tile[1]:
                    return
                xdiff = grid_x - self.game.first_tile[0]
                ydiff = grid_y - self.game.first_tile[1]
                new_x = 0
                new_y = 0
                if abs(xdiff) > abs(ydiff):
                    # horizontal
                    new_x = 1 if xdiff > 0 else -1
                else:
                    # vertical
                    new_y = 1 if ydiff > 0 else -1
                grid_x, grid_y = self.game.first_tile[0] + new_x, self.game.first_tile[1] + new_y
                tile1: Tile = self.game.board[self.game.first_tile[0]][self.game.first_tile[1]]
                tile2: Tile = self.game.board[grid_x][grid_y]
                if (not tile1 or tile1.can_be_moved()) and (not tile2 or tile2.can_be_moved()):
                    if self.game.steps_left > 0:
                        self.game.steps_left -= 1
                        # swap_tiles(self.game, self.game.first_tile, (grid_x, grid_y), self.game.ANIMATION_SPEED)
                        first = self.grid[self.game.first_tile[0]][self.game.first_tile[1]]
                        second = self.grid[grid_x][grid_y]
                        first.tile, second.tile = second.tile, first.tile
                        first.update_rect()
                        second.update_rect()
                self.game.chain_size = 0
            self.game.first_tile = None


class SquareCrushApp(App):
    def build(self):
        global WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE
        if platform == 'android':
            WINDOW_WIDTH = 1080
            WINDOW_HEIGHT = 1920
            TILE_SIZE = WINDOW_WIDTH / GRID_SIZE_X
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        return SquareCrush()


if __name__ == '__main__':
    SquareCrushApp().run()
