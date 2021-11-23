from src.grammars.sentence import Sentence
from src.utils.derivation_unit import DerivationUnit
from src.utils.tm_to_unrestricted import TMToUnrestricted

from src.grammars.symbol import Symbol
from src.grammars.variable import Variable
from src.grammars.terminal import Terminal
from src.grammars.production import Production

from src.grammars.unrestricted_grammar import UnrestrictedGrammar

from src.machines.state import State

from typing import Set, List

from collections import deque

__all__ = ["WordUtils"]


class WordUtils:
    eps_blank_symbol = Variable(f"[{TMToUnrestricted.EPS}|{TMToUnrestricted.BLANK}]")

    @staticmethod
    def is_word_hieroglyph(symbol: Symbol):
        return (
            "[" in symbol.get_value()
            and symbol.get_value() != WordUtils.eps_blank_symbol.get_value()
        )

    @staticmethod
    def accepts(ug: UnrestrictedGrammar, word: str):
        term_sentence = Sentence([Terminal(x) for x in word])
        init_sentence = Sentence([ug.start_symbol])

        derivation_sequence = dict()
        queue = deque([init_sentence])

        while queue:
            sentence = queue.popleft()
            if sentence not in derivation_sequence:
                derivation_sequence[sentence] = list()

            if sentence.is_terminal():
                eps_free_sentence = sentence.remove_epsilons()
                if eps_free_sentence == term_sentence:
                    return derivation_sequence[sentence]
                if len(eps_free_sentence.objects) > len(term_sentence.objects):
                    return None

            for production in filter(
                lambda p: len(p.head) <= len(sentence.objects), ug.productions
            ):
                for i in range(len(sentence.objects) - len(production.head) + 1):
                    start = i
                    final = i + len(production.head)
                    if production.head == sentence.objects[start:final]:
                        next_sentence = Sentence(
                            sentence.objects[:start]
                            + production.body
                            + sentence.objects[final:]
                        )
                        if next_sentence not in derivation_sequence:
                            derivation_sequence[next_sentence] = derivation_sequence[
                                sentence
                            ] + [
                                DerivationUnit(
                                    production=production, sentence=next_sentence
                                )
                            ]
                            queue.append(next_sentence)
            queue = deque(
                sorted(
                    queue,
                    key=lambda sentence: sum(
                        1 for obj in sentence.objects if isinstance(obj, Variable)
                    ),
                )
            )
        return None
