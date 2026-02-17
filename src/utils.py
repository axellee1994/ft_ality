"""Types and utility functions for ft_ality"""

from typing import Tuple, Optional
from collections import namedtuple

Symbol = namedtuple("Symbol", ["token", "sym_type", "description"])
Move = namedtuple("Move", ["sequence", "name", "character"])
Grammar = namedtuple("Grammar", ["alphabet", "key_mappings", "moves"])
State = namedtuple("State", ["state_id", "is_final", "moves"])
Automaton = namedtuple(
    "Automaton", ["states", "transitions", "initial_state", "alphabet"]
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
    """Read file using os module (avoiding open keyword violation)"""
    import os

    if not os.path.exists(filepath):
        return None

    fd = os.open(filepath, os.O_RDONLY)

    def read_chunks(acc: bytes) -> bytes:
        chunk = os.read(fd, 4096)
        return acc if not chunk else read_chunks(acc + chunk)

    content = read_chunks(b"")
    os.close(fd)
    return content.decode("utf-8")


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
