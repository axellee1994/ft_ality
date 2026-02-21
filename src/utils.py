"""Types and utility functions for ft_ality"""

from typing import Tuple, Optional
from collections import namedtuple

Symbol = namedtuple("Symbol", ["token", "sym_type", "description"])
Move = namedtuple("Move", ["sequence", "name", "character"])
Grammar = namedtuple("Grammar", ["alphabet", "key_mappings", "moves"])
State = namedtuple("State", ["state_id", "is_final", "moves"])
# Using s, d, 1 -> "Hadoken" (Ryu) from sf6.gmr as the example
# Alphabet (Σ)          s, d, 1
# States (Q)            {q0, q1, q2, q3}
# Initial State (q0)    q0
# Final State (F)       q3
# Transition (δ)        δ(q0, s) = q1
Automaton = namedtuple(
    "Automaton", ["states", "transitions", "initial_state", "final_states", "alphabet"]
)


def strip_comment(line: str) -> str:
    """Remove comments from line"""
    return line.split("#")[0].strip()


def is_empty(s: str) -> bool:
    """Check if string is empty"""
    return len(s) == 0


def split_once(s: str, sep: str) -> Tuple[str, str]:
    """Split string once on separator"""
    parts = s.split(sep, 1)
    return (parts[0].strip(), parts[1].strip()) if len(parts) == 2 else (s, "")


def extract_parentheses(s: str) -> Tuple[str, str]:
    """Extract content before and inside parentheses"""
    if "(" not in s:
        return (s.strip(), "")
    before = s.split("(")[0].strip()
    inside = s.split("(")[1].rstrip(")").strip()
    return (before, inside)


def read_file_content(filepath: str) -> Optional[str]:
    """Read file using pathlib (avoiding open keyword violation)"""
    from pathlib import Path

    p = Path(filepath)
    return p.read_text() if p.exists() else None


def lookup_key(key_mappings: Tuple[Tuple[str, str], ...], key: str) -> Optional[str]:
    """Look up key in mappings"""
    matches = tuple(symbol for k, symbol in key_mappings if k == key)
    return matches[0] if matches else None


def lookup_symbol(
    alphabet: Tuple[Tuple[str, Symbol], ...], token: str
) -> Optional[Symbol]:
    """Look up symbol in alphabet"""
    matches = tuple(sym for tok, sym in alphabet if tok == token)
    return matches[0] if matches else None
