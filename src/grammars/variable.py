from src.grammars.symbol import Symbol

__all__ = ["Variable"]


class Variable(Symbol):
    def __init__(self, value):
        super(Variable, self).__init__(value)

    def __eq__(self, other: "Variable"):
        if isinstance(other, Variable):
            return self.get_value() == other.get_value()
        return self.get_value() == other

    def __hash__(self):
        return hash(self.get_value())
