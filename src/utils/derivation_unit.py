from src.grammars.symbol import Symbol
from src.grammars.production import Production

from typing import List

__all__ = ["DerivationUnit"]


class DerivationUnit:
    def __init__(self, production: Production, sentence: List[Symbol]):
        self._production = production
        self._sentence = sentence

    @property
    def production(self):
        return self._production

    @property
    def sentence(self):
        return self._sentence
