"""ft_ality - Finite-State Automaton for fighting game move recognition"""

from .utils import Symbol, Move, Grammar, State, Automaton
from .parser import parse_grammar
from .automaton import build_automaton
from .recognition import recognize_sequence
from .interactive import run_interactive_mode
from .display import display_key_mappings, display_moves
from .utils import read_file_content

__all__ = [
    "Symbol",
    "Move",
    "Grammar",
    "State",
    "Automaton",
    "parse_grammar",
    "build_automaton",
    "recognize_sequence",
    "display_key_mappings",
    "display_moves",
    "run_interactive_mode",
    "read_file_content",
]
