# Farben
COLORS = [
	(153, 102, 255),  # lila
	# (255, 127, 80),  # rot
	(255, 215, 0),  # gelb
	(255, 182, 193),  # pink
	(64, 224, 208),  # türkis
	# (218, 112, 214),  # dunkelpink
	# (240, 230, 140),  # beige-gelb
	# (255, 165, 0),  # dunkelorange
	(0, 191, 255)  # blau
]


class Tile:
	def __init__(self, color: tuple):
		self.color = color
