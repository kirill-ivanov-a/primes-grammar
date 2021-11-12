from src.grammars.symbol import Symbol

__all__ = ["Variable"]


class Variable(Symbol):
    def __init__(self, value):
        super(Variable, self).__init__(value)

    def __eq__(self, other: "Variable"):
        if self == other:
            return True
        if isinstance(other, Variable):
            return self.get_value() == other.get_value()
