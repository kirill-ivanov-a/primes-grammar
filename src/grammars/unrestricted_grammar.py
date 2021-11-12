__all__ = ["UnrestrictedGrammar"]

from typing import Set

from src.grammars.production import Production
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

    def rename_variables(self) -> "UnrestrictedGrammar":
        raise NotImplementedError("...")

    @property
    def variables(self) -> Set[Variable]:
        """Get the head variable"""
        return self._variables

    @property
    def terminals(self) -> Set[Terminal]:
        """Get the head variable"""
        return self._terminals

    @property
    def productions(self) -> Set[Production]:
        """Get the head variable"""
        return self._productions

    @property
    def start_symbol(self) -> Variable:
        """Get the head variable"""
        return self._start_symbol
