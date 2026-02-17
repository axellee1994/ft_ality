"""Interactive mode for ft_ality"""

from typing import Tuple
from .utils import Grammar, Automaton
from .utils import is_empty
from .recognition import process_key_input


def run_interactive_mode(
    grammar: Grammar, automaton: Automaton, debug: bool = False
) -> None:
    """Run interactive recognition mode"""
    print("\nTraining Mode")
    print("Enter keys separated by spaces to execute moves")
    print("Press Ctrl+C to exit\n")

    def process_keys(
        buf: Tuple[str, ...], remaining: Tuple[str, ...]
    ) -> Tuple[str, ...]:
        if not remaining:
            return buf
        new_buf, _ = process_key_input(remaining[0], grammar, automaton, buf, debug)
        return process_keys(new_buf, remaining[1:])

    def input_loop(buffer: Tuple[str, ...]) -> None:
        try:
            line = input("> ").strip()
            if is_empty(line):
                input_loop(buffer)
                return
            keys = tuple(line.split())
            final_buffer = process_keys(buffer, keys)
            input_loop(final_buffer)
        except EOFError:
            return
        except KeyboardInterrupt:
            return

    input_loop(())
