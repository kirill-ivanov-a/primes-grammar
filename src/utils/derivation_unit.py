from src.grammars.production import Production
from src.grammars.sentence import Sentence

__all__ = ["DerivationUnit"]


class DerivationUnit:
    def __init__(self, production: Production, sentence: Sentence):
        self._production = production
        self._sentence = sentence

    @property
    def production(self):
        return self._production

    @property
    def sentence(self):
        return self._sentence
