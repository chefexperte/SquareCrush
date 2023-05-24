from __future__ import annotations

import math


def translate_coords(x, y, winkel_grad, distanz):
	winkel_rad = math.radians(winkel_grad)
	delta_x = distanz * math.cos(winkel_rad)
	delta_y = distanz * math.sin(winkel_rad)
	x_neu = x + delta_x
	y_neu = y + delta_y
	return x_neu, y_neu



