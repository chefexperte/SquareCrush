from abc import ABC, abstractmethod


class SQFont(ABC):

    font = None

    @abstractmethod
    def __init__(self, **kwargs):
        pass


class SQDrawable(ABC):
    pass

    # @abstractmethod
    # def draw(self, screen: pygame.Surface):
    #     pass
