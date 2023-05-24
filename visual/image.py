import pygame

_image_cache = {}


def load_image(name: str, size: tuple[int, int] | None = None) -> pygame.Surface:
	if name not in _image_cache:
		_image_cache[name] = pygame.image.load(f"assets/{name}.png")
	image = _image_cache[name]
	if size is not None:
		image = resize(image, *size)
	return image


def colorize(image: pygame.Surface, color: tuple[int, int, int]) -> pygame.Surface:
	# image = image.copy()
	image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
	return image


def resize(image: pygame.Surface, width: int, height: int) -> pygame.Surface:
	return pygame.transform.scale(image, (width, height))
