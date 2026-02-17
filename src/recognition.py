"""Recognition and key-processing functions for ft_ality"""

from typing import Tuple
from .utils import Grammar, Automaton, Move
from .utils import lookup_key
from .automaton import find_state, find_transition
from .display import display_moves


def state_id_after(automaton: Automaton, sequence: Tuple[str, ...]) -> int:
    """Return state ID reached after processing sequence, or -1 if dead."""

    def traverse(seq: Tuple[str, ...], current: int) -> int:
        if not seq:
            return current
        nxt = find_transition(automaton.transitions, current, seq[0])
        return traverse(seq[1:], nxt) if nxt is not None else -1

    return traverse(sequence, automaton.initial_state)


def recognize_sequence(
    automaton: Automaton, sequence: Tuple[str, ...]
) -> Tuple[bool, Tuple[Move, ...]]:
    """Recognize sequence using automaton (pure function)"""
    sid = state_id_after(automaton, sequence)
    if sid == -1:
        return (False, ())
    state = find_state(automaton.states, sid)
    return (True, state.moves) if state and state.is_final else (False, ())


def _debug_transition(
    automaton: Automaton,
    buffer: Tuple[str, ...],
    symbol: str,
    new_buffer: Tuple[str, ...],
) -> None:
    from_state = state_id_after(automaton, buffer)
    to_state = state_id_after(automaton, new_buffer)
    if to_state != -1:
        print(f'State {from_state}, "{symbol}" -> State {to_state}')


def _debug_end_states(
    automaton: Automaton, seq: Tuple[str, ...], moves: Tuple[Move, ...]
) -> None:
    sid = state_id_after(automaton, seq)
    for move in moves:
        print(f'Found end state for "{move.name} ({move.character})" at: {sid}')


def process_key_input(
    key: str,
    grammar: Grammar,
    automaton: Automaton,
    buffer: Tuple[str, ...],
    debug: bool = False,
) -> Tuple[Tuple[str, ...], bool]:
    """Process single key input. Returns (new_buffer, recognized)."""
    symbol = lookup_key(grammar.key_mappings, key)
    if symbol is None:
        return (buffer, False)

    new_buffer = buffer + (symbol,)
    is_recognized, moves = recognize_sequence(automaton, new_buffer)

    if debug:
        _debug_transition(automaton, buffer, symbol, new_buffer)

    if is_recognized:
        if debug:
            _debug_end_states(automaton, new_buffer, moves)
        print(f"\n{', '.join(new_buffer)}")
        display_moves(moves)
        return ((), True)

    if state_id_after(automaton, new_buffer) != -1:
        return (new_buffer, False)

    single = (symbol,)
    is_recognized_single, moves_single = recognize_sequence(automaton, single)
    if is_recognized_single:
        if debug:
            _debug_transition(automaton, (), symbol, single)
            _debug_end_states(automaton, single, moves_single)
        print(f"\n{', '.join(single)}")
        display_moves(moves_single)
        return ((), True)

    return (single if state_id_after(automaton, single) != -1 else (), False)
