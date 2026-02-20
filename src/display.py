"""Display functions for ft_ality"""

from typing import Tuple
from functools import reduce
from .utils import Grammar, Move, Symbol
from .utils import lookup_symbol


def get_symbol_info(
    alphabet: Tuple[Tuple[str, Symbol], ...], symbol: str
) -> Tuple[str, str]:
    """Get (sym_type, description) for a symbol"""
    sym_obj = lookup_symbol(alphabet, symbol)
    return (sym_obj.sym_type, sym_obj.description) if sym_obj else ("", symbol)


def add_mapping_to_groups(
    alphabet: Tuple[Tuple[str, Symbol], ...],
    acc: Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...],
    mapping: Tuple[str, str],
) -> Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...]:
    """Add a single mapping to type-grouped accumulator"""
    key, symbol = mapping
    sym_type, desc = get_symbol_info(alphabet, symbol)
    existing = tuple((t, items) for t, items in acc if t == sym_type)
    other = tuple((t, items) for t, items in acc if t != sym_type)
    if existing:
        t, items = existing[0]
        return other + ((t, items + ((key, desc),)),)
    return acc + ((sym_type, ((key, desc),)),)


def group_mappings_by_type(
    alphabet: Tuple[Tuple[str, Symbol], ...],
    mappings: Tuple[Tuple[str, str], ...],
) -> Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...]:
    """Group mappings by symbol type, sorted"""
    groups = reduce(
        lambda acc, m: add_mapping_to_groups(alphabet, acc, m), mappings, ()
    )
    return tuple((t, tuple(sorted(items))) for t, items in sorted(groups))


def print_group(sym_type: str, mappings: Tuple[Tuple[str, str], ...]) -> None:
    """Print a single group of key mappings"""
    tuple(map(lambda _: print(f"\n{sym_type}:"), (sym_type,) if sym_type else ()))
    tuple(map(lambda kd: print(f"  {kd[0]} -> {kd[1]}"), mappings))


def display_key_mappings(grammar: Grammar) -> None:
    """Display key mappings grouped by type"""
    print("Key mappings:")
    grouped = group_mappings_by_type(grammar.alphabet, grammar.key_mappings)
    tuple(map(lambda g: print_group(*g), grouped))
    print("\n" + "-" * 50)


def display_moves(moves: Tuple[Move, ...]) -> None:
    """Display recognized moves"""

    def show_move(move: Move) -> None:
        print(f"{move.name} ({move.character}) !!")

    tuple(map(show_move, moves))
