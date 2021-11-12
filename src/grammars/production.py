import enum
from typing import List
from src.grammars.symbol import Symbol

__all__ = ["Production"]


class ExecType(enum.Enum):
    TAPE_GENERATING = 1
    TM_EMULATING = 2
    WORD_RESTORING = 3


class Production:
    """A production"""

    def __init__(
        self,
        head: List[Symbol],
        body: List[Symbol],
        exec_type: ExecType = ExecType.WORD_RESTORING,
    ):
        self._head = head
        self._body = body
        self._exec_type = exec_type

    def __str__(self):
        return " ".join(map(str, self._head)) + " -> " + " ".join(map(str, self._body))

    def __eq__(self, other: "Production"):
        if isinstance(other, Production):
            return self.head == other.head and self.body == other.body
        return False

    def __hash__(self):
        return sum(map(hash, self._body)) + sum(map(hash, self._head))

    @property
    def head(self) -> List[Symbol]:
        """Get the head variable"""
        return self._head

    @property
    def body(self) -> List[Symbol]:
        """Get the body objects"""
        return self._body

    @property
    def exec_type(self) -> ExecType:
        """Get the body objects"""
        return self._exec_type
