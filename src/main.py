from utils.lba_to_csg import lba_to_csg
from utils.tm_to_unrestricted import TMToUnrestricted

from src.machines.turing_machine import TuringMachine, State

from src.grammars.unrestricted_grammar import UnrestrictedGrammar
from src.grammars.variable import Variable

from src.utils.word_utils import WordUtils


def generate_t0(path):
    tm = TuringMachine.from_file(path)
    csg = TMToUnrestricted.convert(tm)
    # csg = csg.rename_variables()
    csg.to_file("t0_out.txt")

    return "t0_out.txt"


def generate_t1(path):
    # tm = TuringMachine.from_file(path)
    # csg = lba_to_csg(lba=tm, alphabet={"1"})
    # csg = csg.rename_variables()
    # csg.to_file("t1_out.txt")

    return "t1_out.txt"


def main(grammar_type="t0", number=17):
    TURING_PATH = "../resources/turing_machine.txt"
    LBA_PATH = "../resources/lba.txt"

    T0_PATH = generate_t0(TURING_PATH)
    T1_PATH = generate_t1(LBA_PATH)

    grammar = None

    with open(T0_PATH if grammar_type == "t0" else T1_PATH) as grammar_file:
        grammar = UnrestrictedGrammar.from_text(grammar_file.read())

    final_state = "is_prime"

    result = WordUtils.contains(
        grammar=grammar,
        n=number,
        final_states={State(final_state)},
        need_derivation=False,
    )

    print(result)

    return 0


if __name__ == "__main__":
    main(grammar_type="t0", number=5)
