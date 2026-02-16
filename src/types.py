"""Type definitions for ft_ality"""

from collections import namedtuple

Symbol = namedtuple("Symbol", ["token", "sym_type", "description"])
Move = namedtuple("Move", ["sequence", "name", "character"])
Grammar = namedtuple("Grammar", ["alphabet", "key_mappings", "moves"])
State = namedtuple("State", ["state_id", "is_final", "moves"])
Automaton = namedtuple(
    "Automaton", ["states", "transitions", "initial_state", "alphabet"]
)
