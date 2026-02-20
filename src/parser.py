from typing import Tuple, Optional
from functools import reduce
from .utils import Symbol, Move, Grammar
from .utils import strip_comment, is_empty, split_once, extract_parentheses


def parse_alphabet_line(line: str) -> Optional[Tuple[str, Symbol]]:
    """Parse single alphabet line into (token, Symbol)"""
    if ":" not in line:
        return None
    token, rest = split_once(line, ":")
    sym_type, description = extract_parentheses(rest)
    return (token, Symbol(token, sym_type, description))


def parse_keymapping_line(line: str) -> Optional[Tuple[str, str]]:
    """Parse single keymapping line into (key, symbol)"""
    if "=" not in line:
        return None

    key, symbol = split_once(line, "=")
    return (key, symbol)


def parse_move_line(line: str) -> Optional[Move]:
    """Parse single move line into Move"""
    if "->" not in line:
        return None
    sequence_part, name_part = split_once(line, "->")
    sequence = tuple(
        token.strip()
        for token in sequence_part.split(",")
        if not is_empty(token.strip())
    )
    name_clean = name_part.strip('"')
    name, character = extract_parentheses(name_clean)
    name = name.strip('"')
    character = character if character else "Unknown"
    return Move(sequence, name, character)


def _section_step(
    acc: Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...], str], line: str
) -> Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...], str]:
    """Single reduce step: classify a line into its grammar section."""
    alpha, keys, mvs, section = acc
    cleaned = strip_comment(line)
    if is_empty(cleaned):
        return acc
    if cleaned.startswith("@"):
        return (alpha, keys, mvs, cleaned[1:])
    if section == "alphabet":
        return (alpha + (cleaned,), keys, mvs, section)
    if section == "keymapping":
        return (alpha, keys + (cleaned,), mvs, section)
    if section == "moves":
        return (alpha, keys, mvs + (cleaned,), section)
    return acc


def partition_sections(
    lines: Tuple[str, ...],
) -> Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]:
    """Partition lines into (alphabet, keymapping, moves) sections"""
    alpha, keys, mvs, _ = reduce(_section_step, lines, ((), (), (), ""))
    return (alpha, keys, mvs)


def parse_section(lines: Tuple[str, ...], parser) -> Tuple:
    """Parse section lines with given parser function"""
    parsed = tuple(parser(line) for line in lines)
    return tuple(item for item in parsed if item is not None)


def parse_grammar(content: str) -> Grammar:
    """I dont like keymapping, but keeping it for failsafe"""
    lines = tuple(content.split("\n"))
    alpha_lines, key_lines, move_lines = partition_sections(lines)
    alphabet = parse_section(alpha_lines, parse_alphabet_line)
    if key_lines:
        key_mappings = parse_section(key_lines, parse_keymapping_line)
    else:
        key_mappings = tuple((token, token) for token, _ in alphabet)
    moves = parse_section(move_lines, parse_move_line)
    return Grammar(alphabet, key_mappings, moves)
