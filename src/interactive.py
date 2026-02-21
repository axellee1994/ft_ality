"""Interactive mode for ft_ality"""

import sys
import tty
import termios
import signal
from functools import reduce
from itertools import takewhile
from typing import Tuple, Callable, Optional
from .utils import Grammar, Automaton
from .recognition import process_key_input


def _iterate(f: Callable, x):
    """Yield x, f(x), f(f(x)), ... indefinitely."""
    yield x
    yield from _iterate(f, f(x))


def trampoline(thunk: Callable) -> None:
    """Drive tail-recursive thunks without growing the call stack"""
    reduce(lambda _, f: f, takewhile(callable, _iterate(lambda f: f(), thunk)), None)


def _setup_terminal(fd: int) -> Tuple:
    """Put terminal into cbreak mode, return old settings."""
    old = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old


def _restore_terminal(fd: int, old_settings: Tuple) -> None:
    """Restore terminal to previous settings."""
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def _make_sigint_handler(fd: int, old_settings: Tuple) -> Callable:
    """Return a SIGINT handler that restores the terminal and exits cleanly."""

    def handler(*_) -> None:
        _restore_terminal(fd, old_settings)
        print("\n\nExiting training mode...")
        sys.exit(0)

    return handler


def _make_loop(grammar: Grammar, automaton: Automaton, debug: bool) -> Callable:
    """Return the tail-recursive loop thunk for interactive key reading."""

    def read_key() -> Optional[str]:
        char = sys.stdin.read(1)
        return char if char else None

    def loop(buffer: Tuple[str, ...]) -> Optional[Callable]:
        key = read_key()
        if key is None:
            return None
        new_buffer, _ = process_key_input(key, grammar, automaton, buffer, debug)
        return lambda: loop(new_buffer)

    return lambda: loop(())


def run_interactive_mode(
    grammar: Grammar, automaton: Automaton, debug: bool = False
) -> None:
    """Run interactive recognition mode"""
    print("\nGame Training/Tutorial Mode")
    print("Press keys to execute moves (Ctrl+C to exit)\n")
    fd = sys.stdin.fileno()
    old = _setup_terminal(fd)
    prev = signal.signal(signal.SIGINT, _make_sigint_handler(fd, old))
    trampoline(_make_loop(grammar, automaton, debug))
    signal.signal(signal.SIGINT, prev)
    _restore_terminal(fd, old)
