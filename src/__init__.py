"""ft_ality - Finite-State Automaton for fighting game move recognition"""

from .types import Symbol, Move, Grammar, State, Automaton
from .parser import parse_grammar
from .automaton import build_automaton
from .interactive import recognize_sequence, run_interactive_mode
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
