__all__ = ["Symbol"]

import abc
from abc import ABC


class Symbol(ABC):
    def __init__(self, value: str = None):
        self.value = value

    def __str__(self):
        return self.value

    @abc.abstractmethod
    def __eq__(self, other: "Symbol"):
        pass

    def get_value(self):
        return self.value

    def __hash__(self):
        return hash(self.get_value())
