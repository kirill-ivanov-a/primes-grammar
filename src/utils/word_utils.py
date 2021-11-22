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


class Node:
    def __init__(
        self, sentence: List[Symbol], depth: int, derivation: List[DerivationUnit]
    ):
        self.sentence = sentence
        self.depth = depth
        self.derivation = derivation


class WordUtils:
    eps_blank_symbol = Variable(f"[{TMToUnrestricted.EPS}|{TMToUnrestricted.BLANK}]")

    @staticmethod
    def is_word_hieroglyph(symbol: Symbol):
        return (
            "[" in symbol.get_value()
            and symbol.get_value() != WordUtils.eps_blank_symbol.get_value()
        )

    @staticmethod
    def contains(
        grammar: UnrestrictedGrammar,
        n: int,
        final_states: Set[State],
        need_derivation: bool,
    ):
        productions = sorted(grammar.productions, key=lambda p: len(p.body))

        head_size_list = list(map(lambda p: len(p.head), productions))
        max_head = max(head_size_list) if len(head_size_list) else None

        queue = deque()
        visited = set()
        queue.append(Node(sentence=[grammar.start_symbol], depth=0, derivation=[]))

        while len(queue):
            node = queue.pop()
            sentence = node.sentence
            found_final = False

            if not need_derivation:
                for final_state in final_states:
                    word_size = WordUtils.get_word_size_if_has_final(
                        sentence, productions, final_state
                    )
                    if word_size is not None:
                        if word_size == n:
                            return node.derivation
                        elif word_size > n:
                            return None

                        found_final = True

            if tuple(sentence) not in visited:
                visited.add(tuple(sentence))

                if found_final:
                    continue

                if (
                    len(
                        list(
                            filter(lambda x: WordUtils.is_word_hieroglyph(x), sentence)
                        )
                    )
                    > n
                ):
                    continue

                if all(map(lambda x: isinstance(x, Terminal), sentence)):
                    if len(sentence) > n:
                        return None
                    elif len(sentence) == n:
                        return node.derivation

                for pos in range(len(sentence)):
                    limit = max_head or (len(sentence) - pos)
                    for part_size in range(1, min(limit, len(sentence) - pos) + 1):
                        for production in productions:
                            head_without_eps = list(
                                filter(
                                    lambda x: x != TMToUnrestricted.EPS, production.head
                                )
                            )
                            if sentence[pos : pos + part_size] == head_without_eps:
                                start, end = sentence[:pos], sentence[pos + part_size :]
                                body_without_eps = list(
                                    filter(
                                        lambda x: x != TMToUnrestricted.EPS,
                                        production.body,
                                    )
                                )

                                new_sentence = start + body_without_eps + end

                                queue.append(
                                    Node(
                                        new_sentence,
                                        node.depth + 1,
                                        [
                                            node.derivation,
                                            DerivationUnit(production, new_sentence),
                                        ],
                                    )
                                )
        return None

    @staticmethod
    def get_word_size_if_has_final(
        sentence: List[Symbol], productions: List[Production], final_state: State
    ):
        if Variable(final_state.value) in sentence:
            for production in productions:
                head = production.head
                if (
                    len(head) == 1
                    and head[0] in sentence
                    and len(production.body) == 1
                    and production.body[0].value == TMToUnrestricted.EPS
                ):
                    sentence = list(filter(lambda x: x != head[0], sentence))

            sentence = list(filter(lambda x: x != WordUtils.eps_blank_symbol, sentence))
            return len(sentence)

        elif any(map(lambda x: final_state.value in x.value, sentence)):
            return len(sentence)
        else:
            return None
