from src.machines.direction import Direction
from src.machines.state import State

__all__ = ["TransitionContext", "Transition"]


class TransitionContext:
    def __init__(self, state: State, tape_symbol: str):
        self.state = state
        self.tape_sym = tape_symbol

    @classmethod
    def from_string(cls, transition_context_string):
        from_state, tape_symbol = transition_context_string.split(",")
        return TransitionContext(state=State(from_state), tape_symbol=tape_symbol)


class Transition:
    def __init__(self, context_to: TransitionContext, direction: Direction):
        self.context_to = context_to
        self.direction = direction

    @classmethod
    def from_string(cls, transition_string):
        symbol_to_direction = {
            "<": Direction.LEFT,
            "-": Direction.STAY,
            ">": Direction.RIGHT,
        }
        to_state, tape_symbol, direction = transition_string.split(",")
        return Transition(
            context_to=TransitionContext(State(to_state), tape_symbol=tape_symbol),
            direction=symbol_to_direction[direction],
        )
