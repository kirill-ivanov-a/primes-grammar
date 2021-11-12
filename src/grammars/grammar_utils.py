from typing import List, Dict

from src import Symbol

__all__ = ["map_names"]


def map_names(seq: List[Symbol], mapper: Dict[Symbol, Symbol]) -> List[Symbol]:
    return list(map(lambda s: mapper[s], seq))
