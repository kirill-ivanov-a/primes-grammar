from itertools import product
from typing import Set

from src.machines.turing_machine import TuringMachine
from src.grammars.unrestricted_grammar import UnrestrictedGrammar
from src.grammars.variable import Variable
from src.grammars.terminal import Terminal
from src.grammars.production import Production
from src.machines.direction import Direction

__all__ = ["lba_to_csg"]


def lba_to_csg(
    lba: TuringMachine,
    alphabet: Set[str],
    L: str = "%",
    R: str = "$",
) -> UnrestrictedGrammar:
    alphabet = {Terminal(symbol) for symbol in alphabet}
    productions = set()
    A1 = Variable("A1")
    A2 = Variable("A2")

    q0 = lba.initial_state.value
    tape_symbols = __get_tape_symbols(lba, L, R)

    __add_initial_productions(alphabet, A1, A2, q0, L, R, productions)
    __add_motion_productions(
        lba.states,
        lba.final_states,
        lba.transitions,
        alphabet,
        tape_symbols,
        L,
        R,
        productions,
    )
    __add_final_state_productions(
        lba.final_states, alphabet, tape_symbols, L, R, productions
    )
    __add_restoring_productions(alphabet, tape_symbols, L, R, productions)

    return UnrestrictedGrammar(productions=productions, start_symbol=A1)


def __add_initial_productions(alphabet, A1, A2, q0, L, R, productions):
    for a in alphabet:
        # 4.1, 4.2, 4.3, |w| > 1
        productions |= {
            Production(
                [A1],
                [__create_variable(q0, L, a, a), A2],
            ),
            Production(
                [A2],
                [__create_variable(a, a), A2],
            ),
            Production(
                [A2],
                [__create_variable(a, a, R)],
            ),
        }


def __add_motion_productions(
    states, final_states, transitions, alphabet, tape_symbols, L, R, productions
):
    for state in states - final_states:
        for ctx, trans in transitions.items():
            q = ctx.state.value
            p = trans.context_to.state.value

            if q != state.value:
                continue

            for X, Z in product(tape_symbols, tape_symbols):
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
                                [__create_variable(q, L, X, a)],
                                [__create_variable(L, p, X, a)],
                            )
                        )
                    elif ctx.tape_sym == X and trans.direction == Direction.LEFT:
                        productions |= {
                            # 5.2
                            Production(
                                [__create_variable(L, q, X, a)],
                                [__create_variable(p, L, Y, a)],
                            ),
                            # 6.2
                            Production(
                                [__create_variable(Z, b), __create_variable(q, X, a)],
                                [__create_variable(p, Z, b), __create_variable(Y, a)],
                            ),
                            # 6.4
                            Production(
                                [
                                    __create_variable(L, Z, b),
                                    __create_variable(q, X, a),
                                ],
                                [
                                    __create_variable(L, p, Z, b),
                                    __create_variable(Y, a),
                                ],
                            ),
                            # 7.3
                            Production(
                                [
                                    __create_variable(Z, b),
                                    __create_variable(q, X, a, R),
                                ],
                                [
                                    __create_variable(p, Z, b),
                                    __create_variable(Y, a, R),
                                ],
                            ),
                            Production(
                                [
                                    __create_variable(L, Z, b),
                                    __create_variable(q, X, a, R),
                                ],
                                [
                                    __create_variable(L, p, Z, b),
                                    __create_variable(Y, a, R),
                                ],
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
                                [__create_variable(X, a, q, R)],
                                [__create_variable(p, X, a, R)],
                            )
                        )
                    elif ctx.tape_sym == X and trans.direction == Direction.RIGHT:
                        productions |= {
                            # 5.3
                            Production(
                                [
                                    __create_variable(L, q, X, a),
                                    __create_variable(Z, b),
                                ],
                                [
                                    __create_variable(L, Y, a),
                                    __create_variable(p, Z, b),
                                ],
                            ),
                            Production(
                                [
                                    __create_variable(L, q, X, a),
                                    __create_variable(Z, b, R),
                                ],
                                [
                                    __create_variable(L, Y, a),
                                    __create_variable(p, Z, b, R),
                                ],
                            ),
                            # 6.1
                            Production(
                                [__create_variable(q, X, a), __create_variable(Z, b)],
                                [__create_variable(Y, a), __create_variable(p, Z, b)],
                            ),
                            # 6.3
                            Production(
                                [
                                    __create_variable(q, X, a),
                                    __create_variable(Z, b, R),
                                ],
                                [
                                    __create_variable(Y, a),
                                    __create_variable(p, Z, b, R),
                                ],
                            ),
                            # 7.1
                            Production(
                                [__create_variable(q, X, a, R)],
                                [__create_variable(Y, a, p, R)],
                            ),
                        }
                    elif (
                        ctx.tape_sym == L
                        and Y == L
                        and trans.direction == Direction.STAY
                    ):
                        productions.add(
                            Production(
                                [__create_variable(q, L, X, a)],
                                [__create_variable(p, L, X, a)],
                            )
                        )
                    elif (
                        ctx.tape_sym == R
                        and Y == R
                        and trans.direction == Direction.STAY
                    ):
                        productions.add(
                            Production(
                                [__create_variable(X, a, q, R)],
                                [__create_variable(X, a, p, R)],
                            )
                        )
                    elif ctx.tape_sym == X and trans.direction == Direction.STAY:
                        productions.add(
                            Production(
                                [__create_variable(q, X, a)],
                                [__create_variable(p, Y, a)],
                            )
                        )


def __add_final_state_productions(
    final_states, alphabet, tape_symbols, L, R, productions
):
    # 8.1 -- 8.5
    for q in {st.value for st in final_states}:
        for X in tape_symbols:
            for a in alphabet:
                productions |= {
                    Production(
                        [__create_variable(q, L, X, a)],
                        [a],
                    ),
                    Production(
                        [__create_variable(L, q, X, a)],
                        [a],
                    ),
                    Production(
                        [__create_variable(q, X, a)],
                        [a],
                    ),
                    Production(
                        [__create_variable(q, X, a, R)],
                        [a],
                    ),
                    Production(
                        [__create_variable(X, a, q, R)],
                        [a],
                    ),
                }


def __add_restoring_productions(alphabet, tape_symbols, L, R, productions):
    # 9.1 -- 9.5
    for X in tape_symbols:
        for a, b in product(alphabet, alphabet):
            productions |= {
                Production([a, __create_variable(X, b)], [a, b]),
                Production(
                    [a, __create_variable(X, b, R)],
                    [a, b],
                ),
                Production(
                    [__create_variable(X, a), b],
                    [a, b],
                ),
                Production(
                    [__create_variable(L, X, a), b],
                    [a, b],
                ),
            }


def __create_variable(*string_values):
    return Variable("[" + ",".join(map(str, string_values)) + "]")


def __get_tape_symbols(lba: TuringMachine, left: str, right: str):
    possible_tape_symbols = set()
    for ctx, trans in lba.transitions.items():
        ctx_symbol = ctx.tape_sym
        trans_symbol = trans.context_to.tape_sym

        if ctx_symbol not in {left, right}:
            possible_tape_symbols.add(ctx_symbol)
        if trans_symbol not in {left, right}:
            possible_tape_symbols.add(trans_symbol)
    return possible_tape_symbols
