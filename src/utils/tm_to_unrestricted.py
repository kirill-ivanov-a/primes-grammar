from src.machines.turing_machine import TuringMachine
from src.grammars.unrestricted_grammar import UnrestrictedGrammar
from src.grammars.variable import Variable
from src.grammars.terminal import Terminal
from src.grammars.production import Production
from src.machines.direction import Direction

__all__ = ["TMToUnrestricted"]


class TMToUnrestricted:
    SIGMA = {"1"}
    EPS = "$"
    BLANK = "_"
    SIGMA_EPS = SIGMA | set(EPS)

    @staticmethod
    def convert(tm: TuringMachine):
        """
        Построение основано на:

        Мартыненко Б.К. Языки и трансляции:
        Учеб. пособие — Изд. 2-е, испр. и доп. — СПб.:
        Изд-во С.-Петерб. ун-та, 2013. 265 с.
        """
        gamma = TMToUnrestricted.__get_tape_symbols(tm)

        s = Variable("S")
        s1 = Variable("S1")
        s2 = Variable("S2")
        s3 = Variable("S3")

        q0 = Variable(tm.initial_state.value)

        productions = {
            Production(
                [s],
                [s1, q0, s2],
            ),
            Production([s2], [s3]),
            Production(
                [s1],
                [Variable(f"[{TMToUnrestricted.EPS}|{TMToUnrestricted.BLANK}]")],
            ),
            Production(
                [s3],
                [Variable(f"[{TMToUnrestricted.EPS}|{TMToUnrestricted.BLANK}]")],
            ),
            Production([s1], [Variable(TMToUnrestricted.EPS)]),
            Production([s3], [Variable(TMToUnrestricted.EPS)]),
        }

        for symbol in TMToUnrestricted.SIGMA:
            productions.add(
                Production(
                    [s2],
                    [
                        Variable(f"[{symbol}|{symbol}]"),
                        s2,
                    ],
                )
            )

        for a in TMToUnrestricted.SIGMA_EPS:
            for context in tm.transitions.keys():
                tr = tm.transitions[context]

                state_from_sym = Variable(context.state.value)
                state_to_sym = Variable(tr.context_to.state.value)
                d_sym = Variable(tr.context_to.tape_sym)
                context_sym = Variable(f"[{a}|{context.tape_sym}]")
                context_to_sym = Variable(f"[{a}|{d_sym.value}]")

                if tr.direction == Direction.LEFT:
                    for left_sym in gamma:
                        for bVal in TMToUnrestricted.SIGMA_EPS:
                            context_left_sym = Variable(f"[{bVal}|{left_sym}]")

                            head = [context_left_sym, state_from_sym, context_sym]
                            body = [state_to_sym, context_left_sym, context_to_sym]
                            productions.add(Production(head, body))

                elif tr.direction == Direction.STAY:
                    head = [state_from_sym, context_sym]
                    body = [state_to_sym, context_to_sym]
                    productions.add(Production(head, body))

                elif tr.direction == Direction.RIGHT:
                    head = [state_from_sym, context_sym]
                    body = [context_to_sym, state_to_sym]
                    productions.add(Production(head, body))

        for final_state in tm.final_states:
            q_sym = Variable(final_state.value)

            for cVal in gamma:
                for a in TMToUnrestricted.SIGMA_EPS:
                    a_sym = Terminal(a)
                    context_sym = Variable(f"[{a}|{cVal}]")
                    head = [context_sym, q_sym]
                    body = [q_sym, a_sym, q_sym]
                    productions.add(Production(head, body))

                    head = [q_sym, context_sym]
                    productions.add(Production(head, body))

            head = [q_sym]
            body = [Terminal(TMToUnrestricted.EPS)]
            productions.add(Production(head, body))

        return UnrestrictedGrammar(productions=productions, start_symbol=s)

    @staticmethod
    def __get_tape_symbols(tm: TuringMachine):
        tape_symbols = set()

        for context, transition in tm.transitions.items():
            tape_symbols.add(transition.context_to.tape_sym)
            tape_symbols.add(context.tape_sym)

        return tape_symbols
