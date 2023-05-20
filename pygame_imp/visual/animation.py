from __future__ import annotations

from typing import Callable

import pygame

from universal.consts import TILE_SIZE, BOARD_OFFSET
from pygame_imp.draw import draw_rotated_rect
from tile import Tile, TileAddon
from universal.visual.animation import Animation, TileAnimation
from universal.wrapper import SQDrawable


class PgSurface(pygame.Surface, SQDrawable):
    pass


def tile_to_real_pos(pos: tuple[float, float]) -> tuple[float, float]:
    return (pos[0] + 0.5) * TILE_SIZE + BOARD_OFFSET[0], (pos[1] + 0.5) * TILE_SIZE + BOARD_OFFSET[1]


class PgAnimation(Animation):
    def __init__(self, surface: PgSurface, color: tuple[int, int, int] = (255, 255, 255), start: tuple = (-1, -1),
                 end: tuple = (-1, -1), anim_type: str = "lin", speed: float = 2.5, delay: float = 0,
                 priority: int = 0):
        self.surface = surface
        Animation.__init__(self, surface, color, start, end, anim_type, speed, delay, priority)

    surface: PgSurface = None

    def draw(self, screen: PgSurface):
        x0, y0, angle0, size0 = self.start
        x1, y1, angle1, size1 = self.curr
        x2, y2, angle2, size2 = self.end
        rect_surface = self.surface.copy()

        # Rechteck um den Winkel drehen
        rotated_surface = pygame.transform.rotate(rect_surface, angle1)
        rotated_rect = rotated_surface.get_rect(center=tile_to_real_pos((x1, y1)))
        rotated_rect.scale_by(size1)
        # Rotiertes Rechteck auf dem Bildschirm anzeigen
        # game.screen.blit(rotated_surface, rotated_rect)
        screen.blit(rotated_surface, rotated_rect)


class PgTileAnimation(PgAnimation, TileAnimation):
    def __init__(self, tile: Tile = Tile((0, 0, 0)), start: tuple = (-1, -1),
                 end: tuple = (-1, -1), anim_type: str = "lin", speed: float = 2.5, delay: float = 0):
        surface = PgSurface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        color = tile.color if tile else None
        if len(start) != len(end):
            raise ValueError("Start and end tuples have to be the same length")
        TileAnimation.__init__(self, tile, start, end, anim_type, speed, delay)
        PgAnimation.__init__(self, surface, color, start, end, anim_type, speed, delay)

    def draw(self, screen: PgSurface):
        x0, y0, angle0, size0 = self.start
        x1, y1, angle1, size1 = self.curr
        x2, y2, angle2, size2 = self.end
        if self.tile:
            draw_rotated_rect(screen, self.tile.color, tile_to_real_pos((x1, y1)),
                              TILE_SIZE * size1, TILE_SIZE * size1, angle1)
            if self.tile.addon == TileAddon.BLOCKER:
                draw_rotated_rect(screen, (0, 0, 0), tile_to_real_pos((x1, y1)),
                                  TILE_SIZE * size1, TILE_SIZE * size1, angle1, 200)
