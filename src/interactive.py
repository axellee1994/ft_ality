"""Interactive mode for ft_ality"""

import sys
import tty
import termios
from typing import Tuple, Callable, Optional
from .utils import Grammar, Automaton
from .recognition import process_key_input


def trampoline(thunk: Callable) -> None:
    """Drive tail-recursive thunks without growing the call stack"""
    result = thunk
    while callable(result):
        result = result()


def run_interactive_mode(
    grammar: Grammar, automaton: Automaton, debug: bool = False
) -> None:
    """Run interactive recognition mode"""
    print("\nGame Training/Tutorial Mode")
    print("Press keys to execute moves (Ctrl+C to exit)\n")

    def read_key() -> str:
        return sys.stdin.read(1)

    def loop(buffer: Tuple[str, ...]) -> Optional[Callable]:
        key = read_key()
        if not key:
            return None
        new_buffer, _ = process_key_input(key, grammar, automaton, buffer, debug)
        return lambda: loop(new_buffer)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        trampoline(lambda: loop(()))
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
