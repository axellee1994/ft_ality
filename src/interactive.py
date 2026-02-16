"""Interactive mode and recognition functions for ft_ality"""

from typing import Tuple

from .types import Grammar, Automaton, Move
from .utils import is_empty, lookup_key
from .automaton import find_state, find_transition
from .display import display_moves


def recognize_sequence(
    automaton: Automaton, sequence: Tuple[str, ...]
) -> Tuple[bool, Tuple[Move, ...]]:
    """Recognize sequence using automaton (pure function)"""

    def traverse(seq: Tuple[str, ...], current: int) -> int:
        if not seq:
            return current

        next_state = find_transition(automaton.transitions, current, seq[0])
        if next_state is None:
            return -1

        return traverse(seq[1:], next_state)

    final_state_id = traverse(sequence, automaton.initial_state)

    if final_state_id == -1:
        return (False, ())

    final_state = find_state(automaton.states, final_state_id)

    if final_state and final_state.is_final:
        return (True, final_state.moves)

    return (False, ())


def process_key_input(
    key: str, grammar: Grammar, automaton: Automaton, buffer: Tuple[str, ...]
) -> Tuple[Tuple[str, ...], bool]:
    """Process single key input (pure logic with I/O side effects)"""
    symbol = lookup_key(grammar.key_mappings, key)

    if symbol is None:
        return (buffer, False)

    new_buffer = buffer + (symbol,)
    is_recognized, moves = recognize_sequence(automaton, new_buffer)

    if is_recognized:
        print(f"\n{', '.join(new_buffer)}")
        display_moves(moves)
        return (new_buffer, True)

    return (new_buffer, False)


def run_interactive_mode(grammar: Grammar, automaton: Automaton) -> None:
    """Run interactive recognition mode"""
    print("\nTraining Mode")
    print("Enter keys separated by spaces to execute moves")
    print("Press Ctrl+C to exit\n")

    def input_loop(buffer: Tuple[str, ...]) -> None:
        try:
            line = input("> ").strip()
            if is_empty(line):
                input_loop(buffer)
                return

            keys = tuple(line.split())

            def process_keys(
                buf: Tuple[str, ...], remaining: Tuple[str, ...]
            ) -> Tuple[str, ...]:
                if not remaining:
                    return buf

                new_buf, _ = process_key_input(remaining[0], grammar, automaton, buf)
                return process_keys(new_buf, remaining[1:])

            final_buffer = process_keys((), keys)
            input_loop(())

        except EOFError:
            return
        except KeyboardInterrupt:
            return

    input_loop(())
