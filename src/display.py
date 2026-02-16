"""Display functions for ft_ality"""

from typing import Tuple
from .types import Grammar, Move
from .utils import lookup_symbol


def display_key_mappings(grammar: Grammar) -> None:
    """Display key mappings grouped by type (I/O function)"""

    def get_info(symbol: str) -> Tuple[str, str]:
        """Get type and description for a symbol"""
        sym_obj = lookup_symbol(grammar.alphabet, symbol)
        if sym_obj:
            return (sym_obj.sym_type, sym_obj.description)
        return ("", symbol)

    def group_by_type(
        mappings: Tuple[Tuple[str, str], ...],
    ) -> Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...]:
        """Group mappings by symbol type"""
        from functools import reduce

        def add_to_groups(
            acc: Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...],
            mapping: Tuple[str, str],
        ) -> Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...]:
            key, symbol = mapping
            sym_type, desc = get_info(symbol)

            existing = tuple((t, items) for t, items in acc if t == sym_type)
            other = tuple((t, items) for t, items in acc if t != sym_type)

            if existing:
                t, items = existing[0]
                return other + ((t, items + ((key, desc),)),)
            else:
                return acc + ((sym_type, ((key, desc),)),)

        groups = reduce(add_to_groups, mappings, ())
        return tuple((t, tuple(sorted(items))) for t, items in sorted(groups))

    print("Controls:")
    grouped = group_by_type(grammar.key_mappings)

    for sym_type, mappings in grouped:
        if sym_type:
            print(f"\n{sym_type}:")
        for key, desc in mappings:
            print(f"  {key} -> {desc}")

    print("\n" + "-" * 50)


def display_moves(moves: Tuple[Move, ...]) -> None:
    """Display recognized moves (I/O function)"""

    def show_move(move: Move) -> None:
        print(f"{move.name} ({move.character}) !!")

    tuple(map(show_move, moves))
