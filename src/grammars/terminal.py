from src.grammars.symbol import Symbol

__all__ = ["Terminal"]


class Terminal(Symbol):
    def __init__(self, value):
        super(Terminal, self).__init__(value)

    def __eq__(self, other: "Terminal"):
        if self == other:
            return True
        if isinstance(other, Terminal):
            return self.get_value() == other.get_value()
