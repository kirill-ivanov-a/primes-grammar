from typing import Set, Dict

from src.machines.state import State
from src.machines.transition import TransitionContext, Transition

__all__ = ["TuringMachine"]


class TuringMachine:
    def __init__(
        self,
        states: Set[State] = None,
        initial_state: State = None,
        final_states: Set[State] = None,
        transitions: Dict[TransitionContext, Transition] = None,
    ):
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    @classmethod
    def from_file(cls, filename):
        configuration_file = open(filename, "r")

        states = set()
        initial_state = None
        final_states = set()
        transitions = dict()

        for line in configuration_file:
            if line.startswith("initial_state"):
                initial_state = line.split("=")[1].strip()
            elif line.startswith("final_states"):
                rhs = line.split("=")[1]
                final_states = set(map(lambda x: x.strip(), rhs.split(",")))
            elif line.startswith("#") or line == "\n":
                continue
            else:
                prev_transition_context_string, transition_string = map(
                    lambda x: x.strip(), line.split("==>")
                )
                states.add(prev_transition_context_string.split(",")[0])

                prev_transition_context = TransitionContext.from_string(
                    prev_transition_context_string
                )
                transition = Transition.from_string(transition_string)

                transitions.update({prev_transition_context: transition})

        configuration_file.close()

        return TuringMachine(
            states=states,
            initial_state=initial_state,
            final_states=final_states,
            transitions=transitions,
        )
