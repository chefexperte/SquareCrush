from abc import abstractmethod, ABC
from typing import Callable

from universal.wrapper import SQFont, SQDrawable


class UIObject(ABC):

    on_hover: Callable[[bool], None]
    on_click: Callable
    hovering: bool = False

    def __init__(self, on_hover: Callable = None, on_click: Callable = None, ident: str = None):
        self.on_hover: Callable[[bool], None] = on_hover
        self.on_click: Callable = on_click
        if not ident:
            ident = str(id(self))
        # REGISTRY[ident] = self

    def hover(self, yes: bool):
        self.hovering = yes
        if self.on_hover:
            self.on_hover(yes)

    def click(self):
        if self.on_click:
            self.on_click()

    @abstractmethod
    def draw(self, screen: SQDrawable):
        pass


class UILabel(UIObject, ABC):

    _text: str
    font: SQFont
    color: tuple[int, int, int]

    def __init__(self, text: str, font: SQFont, color: tuple[int, int, int], pos: tuple[float, float],
                 on_hover: Callable = None, on_click: Callable = None, ident: str = None):
        self.font = font
        self.color = color
        self.pos = pos
        self.text = text
        super().__init__(on_hover, on_click, ident)

    def set_text(self, text: str) -> None:
        self._text = text

    text: str = property(lambda self: self._text, set_text)
