__all__ = ["UnrestrictedGrammar"]

from typing import Set, Tuple

from src.grammars.grammar_utils import map_names
from src.grammars.production import Production
from src.grammars.unrestricted_grammar_exceptions import (
    InvalidUnrestrictedGrammarFormatException,
)
from src.grammars.variable import Variable
from src.grammars.terminal import Terminal


class UnrestrictedGrammar:
    def __init__(
        self,
        variables: Set[Variable] = None,
        terminals: Set[Terminal] = None,
        productions: Set[Production] = None,
        start_symbol: Variable = None,
    ):
        self._variables = variables if variables else set()
        self._terminals = terminals if terminals else set()
        self._productions = productions if productions else set()
        self._start_symbol = start_symbol if start_symbol else Variable("S")

        if productions:
            for p in productions:
                for symbol in p.head + p.body:
                    if isinstance(symbol, Variable):
                        self._variables.add(symbol)
                    elif isinstance(symbol, Terminal):
                        self._terminals.add(symbol)

    @property
    def variables(self) -> Set[Variable]:
        return self._variables

    @property
    def terminals(self) -> Set[Terminal]:
        return self._terminals

    @property
    def productions(self) -> Set[Production]:
        return self._productions

    @property
    def start_symbol(self) -> Variable:
        return self._start_symbol

    def rename_variables(self) -> "UnrestrictedGrammar":
        mapper = {v: Variable(f"S{i}") for i, v in enumerate(self._variables)}
        mapper.update(zip(self._terminals, self._terminals))

        new_productions = {
            Production(map_names(p.head, mapper), map_names(p.body, mapper))
            for p in self._productions
        }
        new_start_symbol = mapper[self._start_symbol]

        return UnrestrictedGrammar(
            productions=new_productions, start_symbol=new_start_symbol
        )

    def to_text(self) -> str:
        return "\n".join(str(p) for p in self.productions)

    def to_file(self, path):
        with open(path, "w") as output:
            output.write(self.to_text())

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")) -> "UnrestrictedGrammar":
        productions = set()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise InvalidUnrestrictedGrammarFormatException(
                    "There should be only one production per line."
                )

            head_text, body_text = production_objects
            head = [
                Variable(symbol) if symbol.isupper() else Terminal(symbol)
                for symbol in head_text.strip()
            ]
            body = [
                Variable(symbol) if symbol.isupper() else Terminal(symbol)
                for symbol in head_text.strip()
            ]

            if not any(isinstance(s, Variable) for s in head):
                raise InvalidUnrestrictedGrammarFormatException(
                    "There should be at least one variable in head."
                )
            productions.add(Production(head, body))

        return UnrestrictedGrammar(start_symbol=start_symbol, productions=productions)
