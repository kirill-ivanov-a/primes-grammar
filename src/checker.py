#!/usr/bin/python

import pathlib
import sys
import logging

from src.config import Config

from src.utils.word_utils import WordUtils
from src.grammars.unrestricted_grammar import UnrestrictedGrammar
from src.machines.turing_machine import TuringMachine
from src.utils.tm_to_unrestricted import TMToUnrestricted
from src.utils.lba_to_csg import lba_to_csg


def __generate_grammar(grammar_type, path):
    tm = TuringMachine.from_file(
        filename=Config.TURING_MACHINE_PATH if grammar_type == "t0" else Config.LBA_PATH
    )
    csg = None
    if grammar_type == "t0":
        csg = TMToUnrestricted.convert(tm)
    elif grammar_type == "t1":
        csg = lba_to_csg(lba=tm, alphabet={"1"})

    csg = csg.rename_variables()

    csg.to_file(path)

    return pathlib.Path(path)


def __show_derivation(derivation, start_symbol):
    sys.stdout.write(f"Start symbol: {start_symbol}\n")
    for step in derivation:
        sys.stdout.write(
            f"Used production: {step.production}\nSentence: {step.sentence}\n"
        )


def check_prime(grammar_type, number, derivation):
    grammar_path = None
    if grammar_type == "t0":
        grammar_path = Config.T0_GRAMMAR_PATH
    elif grammar_type == "t1":
        grammar_path = Config.T1_GRAMMAR_PATH

    if Config.GENERATE_GRAMMAR:
        path = __generate_grammar(grammar_type, grammar_path)
        logging.info(
            msg=f" Config.GENERATE_GRAMMAR set True\nGrammar generated at {path}"
        )

    grammar = UnrestrictedGrammar.from_file(path=grammar_path)
    result = WordUtils.accepts(ug=grammar, word="1" * int(number))

    if not result:
        logging.info(msg=f" {number} is not prime")
    else:
        logging.info(msg=f" {number} is prime")
        if derivation == "1":
            __show_derivation(result, start_symbol=grammar.start_symbol.value)

    return 0
