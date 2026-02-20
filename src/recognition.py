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
    tuple(
        map(
            lambda m: print(
                f'Found end state for "{m.name} ({m.character})" at: {sid}'
            ),
            moves,
        )
    )


def emit_recognized(
    automaton: Automaton,
    seq: Tuple[str, ...],
    moves: Tuple[Move, ...],
    debug: bool,
) -> Tuple[Tuple[str, ...], bool]:
    """Print recognized sequence/moves and return empty buffer."""
    if debug:
        _debug_end_states(automaton, seq, moves)
    print(f"\n{', '.join(seq)}")
    display_moves(moves)
    return ((), True)


def try_single(
    symbol: str,
    automaton: Automaton,
    debug: bool,
) -> Tuple[Tuple[str, ...], bool]:
    """Try symbol as a fresh single-token sequence after a dead end."""
    single = (symbol,)
    is_recognized, moves = recognize_sequence(automaton, single)
    if is_recognized:
        if debug:
            _debug_transition(automaton, (), symbol, single)
        return emit_recognized(automaton, single, moves, debug)
    return (single if state_id_after(automaton, single) != -1 else (), False)


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
        return emit_recognized(automaton, new_buffer, moves, debug)
    if state_id_after(automaton, new_buffer) != -1:
        return (new_buffer, False)
    return try_single(symbol, automaton, debug)
