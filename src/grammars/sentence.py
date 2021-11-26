from typing import List
from src.grammars.terminal import Terminal
from src.grammars.symbol import Symbol

__all__ = ["Sentence"]


class Sentence:
    """A sentence"""

    def __init__(
        self,
        sentence: List[Symbol],
    ):
        self._sentence = sentence

    def __str__(self):
        return " ".join(map(str, self._sentence))

    def __repr__(self):
        return str(self)

    def __eq__(self, other: "Sentence"):
        if isinstance(other, Sentence):
            return self._sentence == other._sentence
        return False

    def __hash__(self):
        return sum(map(hash, self._sentence))

    def remove_epsilons(self):
        return self.__class__([obj for obj in self.objects if obj.value != "$"])

    def is_terminal(self):
        return all(isinstance(symb, Terminal) for symb in self._sentence)

    @property
    def objects(self) -> List[Symbol]:
        return self._sentence
