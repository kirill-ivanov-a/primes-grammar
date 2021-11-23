import pathlib
import logging

__all__ = ["Config"]


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


class Config:
    ROOT = pathlib.Path(__file__).parent.parent
    T0_GRAMMAR_PATH = ROOT / "resources" / "unrestricted_grammar_primes.txt"
    T1_GRAMMAR_PATH = ROOT / "resources" / "csg_primes.txt"
    TURING_MACHINE_PATH = ROOT / "resources" / "turing_machine.txt"
    LBA_PATH = ROOT / "resources" / "lba.txt"
    GENERATE_GRAMMAR = True
