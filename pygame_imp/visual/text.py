from pygame_imp.ui_object import PgFont


class GameFonts:
	def __init__(self):
		self.title_font = PgFont(None, 36)
		self.shout_font = PgFont("assets/fonts/ZeroCool/ZeroCool.woff2", 45)
	title_font: PgFont
	shout_font: PgFont
