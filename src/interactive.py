"""Interactive mode for ft_ality"""

import sys
import tty
import termios
from typing import Tuple
from .utils import Grammar, Automaton
from .recognition import process_key_input


def run_interactive_mode(
    grammar: Grammar, automaton: Automaton, debug: bool = False
) -> None:
    """Run interactive recognition mode"""
    print("\nTraining Mode")
    print("Press keys to execute moves (Ctrl+C to exit)\n")

    def read_key() -> str:
        return sys.stdin.read(1)

    def loop(buffer: Tuple[str, ...]) -> None:
        key = read_key()
        if not key:
            return
        new_buffer, _ = process_key_input(key, grammar, automaton, buffer, debug)
        loop(new_buffer)

    sys.setrecursionlimit(10000)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        loop(())
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
