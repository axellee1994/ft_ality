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
        groups = {}
        for key, symbol in mappings:
            sym_type, desc = get_info(symbol)
            if sym_type not in groups:
                groups[sym_type] = []
            groups[sym_type].append((key, desc))
        return tuple((t, tuple(sorted(m))) for t, m in sorted(groups.items()))

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
