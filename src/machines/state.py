__all__ = ["State"]


class State:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        else:
            return self.value == other.value

    def __hash__(self):
        return hash(self.value)
