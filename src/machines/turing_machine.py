from collections import namedtuple
from typing import Set, Dict, NamedTuple

__all__ = ['TuringMachine']


class Direction:
    LEFT = -1
    STAY = 0
    RIGHT = 1


class State:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        else:
            return self.value == other.value


class TransitionContext:
    def __init__(self, state: State, tape_symbol: str):
        self.state = state
        self.tape_sym = tape_symbol

    @classmethod
    def from_string(cls, transition_context_string):
        from_state, tape_symbol = transition_context_string.split(',')
        return TransitionContext(state=State(from_state), tape_symbol=tape_symbol)


class Transition:
    def __init__(self, context_to: TransitionContext, direction: Direction):
        self.context_to = context_to
        self.direction = direction

    @classmethod
    def from_string(cls, transition_string):
        symbol_to_direction = {'<': Direction.LEFT, '-': Direction.STAY, '>': Direction.RIGHT}
        to_state, tape_symbol, direction = transition_string.split(',')
        return Transition(context_to=TransitionContext(State(to_state), tape_symbol=tape_symbol),
                          direction=symbol_to_direction[direction])


class TuringMachine:
    def __init__(self, states: Set[State] = None, initial_state: State = None,
                 final_states: Set[State] = None, transitions: Dict[TransitionContext, Transition] = None):
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    @classmethod
    def from_file(cls, filename):
        configuration_file = open(filename, 'r')

        states = set()
        initial_state = None
        final_states = set()
        transitions = dict()

        for line in configuration_file:
            if line.startswith('initial_state'):
                initial_state = line.split("=")[1].strip()
            elif line.startswith('final_states'):
                rhs = line.split("=")[1]
                final_states = set(map(lambda x: x.strip(), rhs.split(',')))
            elif line.startswith('#') or line == '\n':
                continue
            else:
                prev_transition_context_string, transition_string = map(lambda x: x.strip(), line.split("==>"))
                states.add(prev_transition_context_string.split(',')[0])

                prev_transition_context = TransitionContext.from_string(prev_transition_context_string)
                transition = Transition.from_string(transition_string)

                transitions.update({prev_transition_context: transition})

        configuration_file.close()

        return TuringMachine(states=states, initial_state=initial_state,
                             final_states=final_states, transitions=transitions)
