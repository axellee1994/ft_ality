"""Automaton building functions for ft_ality"""

from typing import Tuple, Optional
from functools import reduce
from .types import State, Automaton, Grammar, Move


def find_state(states: Tuple[State, ...], state_id: int) -> Optional[State]:
    """Find state by ID"""
    matches = tuple(s for s in states if s.state_id == state_id)
    return matches[0] if matches else None


def find_transition(
    transitions: Tuple[Tuple[Tuple[int, str], int], ...], from_state: int, symbol: str
) -> Optional[int]:
    """Find transition target state"""
    matches = tuple(
        target
        for (source, sym), target in transitions
        if source == from_state and sym == symbol
    )
    return matches[0] if matches else None


def add_state(states: Tuple[State, ...], state: State) -> Tuple[State, ...]:
    """Add or update state in states tuple"""
    filtered = tuple(s for s in states if s.state_id != state.state_id)
    return filtered + (state,)


def add_transition(
    transitions: Tuple[Tuple[Tuple[int, str], int], ...],
    from_state: int,
    symbol: str,
    to_state: int,
) -> Tuple[Tuple[Tuple[int, str], int], ...]:
    """Add transition to transitions tuple"""
    key = (from_state, symbol)
    filtered = tuple(t for t in transitions if t[0] != key)
    return filtered + ((key, to_state),)


def build_path_recursive(
    sequence: Tuple[str, ...],
    current: int,
    states: Tuple[State, ...],
    transitions: Tuple[Tuple[Tuple[int, str], int], ...],
    next_id: int,
) -> Tuple[int, Tuple[State, ...], Tuple[Tuple[Tuple[int, str], int], ...], int]:
    """Recursively build path through automaton for a sequence"""
    if not sequence:
        return (current, states, transitions, next_id)

    symbol = sequence[0]
    rest = sequence[1:]

    existing = find_transition(transitions, current, symbol)

    if existing is not None:
        return build_path_recursive(rest, existing, states, transitions, next_id)

    new_state = State(next_id, False, ())
    new_states = add_state(states, new_state)
    new_transitions = add_transition(transitions, current, symbol, next_id)

    return build_path_recursive(rest, next_id, new_states, new_transitions, next_id + 1)


def add_move_to_automaton(
    automaton_data: Tuple[
        Tuple[State, ...], Tuple[Tuple[Tuple[int, str], int], ...], int
    ],
    move: Move,
) -> Tuple[Tuple[State, ...], Tuple[Tuple[Tuple[int, str], int], ...], int]:
    """Add move to automaton (pure function)"""
    states, transitions, next_id = automaton_data

    final_state_id, new_states, new_transitions, new_next_id = build_path_recursive(
        move.sequence, 0, states, transitions, next_id
    )

    final_state = find_state(new_states, final_state_id)
    updated_state = State(
        final_state_id, True, final_state.moves + (move,) if final_state else (move,)
    )

    return (add_state(new_states, updated_state), new_transitions, new_next_id)


def build_automaton(grammar: Grammar) -> Automaton:
    """Build automaton from grammar (pure function)"""
    alphabet = tuple(set(symbol for move in grammar.moves for symbol in move.sequence))
    initial = ((State(0, False, ()),), (), 1)
    states, transitions, _ = reduce(add_move_to_automaton, grammar.moves, initial)
    return Automaton(states, transitions, 0, alphabet)
