import pathlib
import logging

__all__ = ["Config"]

# Config for logger. Is used to output messages in checker.py
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


class Config:
    """
    Config for the primality checker function
    """

    # Path to the root of current project
    ROOT = pathlib.Path(__file__).parent.parent
    # Path to the file where to generate and use T0 grammar
    T0_GRAMMAR_PATH = ROOT / "resources" / "unrestricted_grammar_primes.txt"
    # Path to the file where to generate and use T1 grammar
    T1_GRAMMAR_PATH = ROOT / "resources" / "csg_primes.txt"
    # Path to the initial configuration of Turing Machine
    TURING_MACHINE_PATH = ROOT / "resources" / "turing_machine.txt"
    # Path to the initial configuration of LBA
    LBA_PATH = ROOT / "resources" / "lba.txt"
    # If True, regenerate T0 / T1 grammar on every run
    GENERATE_GRAMMAR = False
