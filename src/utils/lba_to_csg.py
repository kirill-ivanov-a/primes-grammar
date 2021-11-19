from itertools import product
from typing import List, Set

from src.machines.turing_machine import TuringMachine
from src.grammars.unrestricted_grammar import UnrestrictedGrammar
from src.grammars.variable import Variable
from src.grammars.terminal import Terminal
from src.grammars.production import Production, ExecType
from src.machines.direction import Direction


def create_variable(*string_values: str):
    return Variable("[" + ",".join(string_values) + "]")


def get_possible_tape_symbols(lba: TuringMachine, left: str, right: str):
    possible_tape_symbols = set()
    for ctx, trans in lba.transitions.items():
        ctx_symbol = ctx.tape_sym
        trans_symbol = trans.context_to.tape_sym

        if ctx_symbol not in {left, right}:
            possible_tape_symbols.add(ctx_symbol)
        if trans_symbol not in {left, right}:
            possible_tape_symbols.add(trans_symbol)
    return possible_tape_symbols


def lba_to_csg(
    lba: TuringMachine, L: str = "%", R: str = "$", alphabet: Set[str] = None
) -> UnrestrictedGrammar:
    alphabet = {Terminal(symbol) for symbol in alphabet}
    productions = set()
    A1 = Variable("A1")
    A2 = Variable("A2")

    q0 = lba.initial_state.value

    for a in alphabet:
        # 4.1, 4.2, 4.3, |w| > 1
        productions |= {
            Production(
                [A1], [create_variable(q0, L, a, a), A2], ExecType.TAPE_GENERATING
            ),
            Production([A2], [create_variable(a, a), A2], ExecType.TAPE_GENERATING),
            Production([A2], [create_variable(a, a, R)], ExecType.TAPE_GENERATING),
        }
    possible_tape_symbols = get_possible_tape_symbols(lba, L, R)

    for state in lba.states - lba.final_states:
        for ctx, trans in lba.transitions.items():
            q = ctx.state.value
            p = trans.context_to.state.value

            if q != state.value:
                continue

            for X, Z in product(possible_tape_symbols, possible_tape_symbols):
                for a, b in product(alphabet, alphabet):
                    Y = trans.context_to.tape_sym

                    if (
                        ctx.tape_sym == L
                        and Y == L
                        and trans.direction == Direction.RIGHT
                    ):
                        # 5.1
                        productions.add(
                            Production(
                                [create_variable(q, L, X, a)],
                                [create_variable(L, p, X, a)],
                                ExecType.TM_EMULATING,
                            )
                        )
                    elif ctx.tape_sym == X and trans.direction == Direction.LEFT:
                        productions |= {
                            # 5.2
                            Production(
                                [create_variable(L, q, X, a)],
                                [create_variable(p, L, Y, a)],
                                ExecType.TM_EMULATING,
                            ),
                            # 6.2
                            Production(
                                [create_variable(Z, b), create_variable(q, X, a)],
                                [create_variable(p, Z, b), create_variable(Y, a)],
                                ExecType.TM_EMULATING,
                            ),
                            # 6.4
                            Production(
                                [
                                    create_variable(L, Z, b),
                                    create_variable(q, X, a),
                                ],
                                [
                                    create_variable(L, p, Z, b),
                                    create_variable(Y, a),
                                ],
                                ExecType.TM_EMULATING,
                            ),
                            # 7.3
                            Production(
                                [
                                    create_variable(Z, b),
                                    create_variable(q, X, a, R),
                                ],
                                [
                                    create_variable(p, Z, b),
                                    create_variable(Y, a, R),
                                ],
                                ExecType.TM_EMULATING,
                            ),
                            Production(
                                [
                                    create_variable(L, Z, b),
                                    create_variable(q, X, a, R),
                                ],
                                [
                                    create_variable(L, p, Z, b),
                                    create_variable(Y, a, R),
                                ],
                                ExecType.TM_EMULATING,
                            ),
                        }
                    elif (
                        ctx.tape_sym == R
                        and Y == R
                        and trans.direction == Direction.LEFT
                    ):
                        # 7.2
                        productions.add(
                            Production(
                                [create_variable(X, a, q, R)],
                                [create_variable(p, X, a, R)],
                                ExecType.TM_EMULATING,
                            )
                        )
                    elif ctx.tape_sym == X and trans.direction == Direction.RIGHT:
                        productions |= {
                            # 5.3
                            Production(
                                [create_variable(L, q, X, a), create_variable(Z, b)],
                                [create_variable(L, Y, a), create_variable(p, Z, b)],
                                ExecType.TM_EMULATING,
                            ),
                            Production(
                                [create_variable(L, q, X, a), create_variable(Z, b, R)],
                                [create_variable(L, Y, a), create_variable(p, Z, b, R)],
                                ExecType.TM_EMULATING,
                            ),
                            # 6.1
                            Production(
                                [create_variable(q, X, a), create_variable(Z, b)],
                                [create_variable(Y, a), create_variable(p, Z, b)],
                                ExecType.TM_EMULATING,
                            ),
                            # 6.3
                            Production(
                                [create_variable(q, X, a), create_variable(Z, b, R)],
                                [create_variable(Y, a), create_variable(p, Z, b, R)],
                                ExecType.TM_EMULATING,
                            ),
                            # 7.1
                            Production(
                                [create_variable(q, X, a, R)],
                                [create_variable(Y, a, p, R)],
                                ExecType.TM_EMULATING,
                            ),
                        }
                    elif (
                        ctx.tape_sym == L
                        and Y == L
                        and trans.direction == Direction.STAY
                    ):
                        productions.add(
                            Production(
                                [create_variable(q, L, X, a)],
                                [create_variable(p, L, X, a)],
                                ExecType.TM_EMULATING,
                            )
                        )
                    elif (
                        ctx.tape_sym == R
                        and Y == R
                        and trans.direction == Direction.STAY
                    ):
                        productions.add(
                            Production(
                                [create_variable(X, a, q, R)],
                                [create_variable(X, a, p, R)],
                                ExecType.TM_EMULATING,
                            )
                        )
                    elif ctx.tape_sym == X and trans.direction == Direction.STAY:
                        productions.add(
                            Production(
                                [create_variable(q, X, a)],
                                [create_variable(p, Y, a)],
                                ExecType.TM_EMULATING,
                            )
                        )

    # 8.1 -- 8.5
    for q in {st.value for st in lba.final_states}:
        for X in possible_tape_symbols:
            for a in alphabet:
                productions |= {
                    Production(
                        [create_variable(q, L, X, a)],
                        [a],
                        ExecType.WORD_RESTORING,
                    ),
                    Production(
                        [create_variable(L, q, X, a)],
                        [a],
                        ExecType.WORD_RESTORING,
                    ),
                    Production(
                        [create_variable(q, X, a)], [a], ExecType.WORD_RESTORING
                    ),
                    Production(
                        [create_variable(q, X, a, R)],
                        [a],
                        ExecType.WORD_RESTORING,
                    ),
                    Production(
                        [create_variable(X, a, q, R)],
                        [a],
                        ExecType.WORD_RESTORING,
                    ),
                }

    # 9.1 -- 9.5
    for X in possible_tape_symbols:
        for a, b in product(alphabet, alphabet):
            productions |= {
                Production([a, create_variable(X, b)], [a, b], ExecType.WORD_RESTORING),
                Production(
                    [a, create_variable(X, b, R)], [a, b], ExecType.WORD_RESTORING
                ),
                Production([create_variable(X, a), b], [a, b], ExecType.WORD_RESTORING),
                Production(
                    [create_variable(L, X, a), b],
                    [a, b],
                    ExecType.WORD_RESTORING,
                ),
            }

    return UnrestrictedGrammar(productions=productions, start_symbol=A1)
