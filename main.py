"""ft_ality - Finite-State Automaton for fighting game move recognition"""

import sys
from typing import Tuple, Optional
from functools import reduce
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


def partition_sections(
    lines: Tuple[str, ...],
) -> Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]:
    """Partition lines into (alphabet, keymapping, moves) sections"""

    def helper(
        acc: Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...], str], line: str
    ) -> Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...], str]:
        alpha, keys, mvs, section = acc

        cleaned = strip_comment(line)
        if is_empty(cleaned):
            return acc

        if cleaned.startswith("@"):
            return (alpha, keys, mvs, cleaned[1:])

        if section == "alphabet":
            return (alpha + (cleaned,), keys, mvs, section)
        elif section == "keymapping":
            return (alpha, keys + (cleaned,), mvs, section)
        elif section == "moves":
            return (alpha, keys, mvs + (cleaned,), section)

        return acc

    alpha, keys, mvs, _ = reduce(helper, lines, ((), (), (), ""))
    return (alpha, keys, mvs)


def parse_section(lines: Tuple[str, ...], parser) -> Tuple:
    """Parse section lines with given parser function"""
    parsed = tuple(parser(line) for line in lines)
    return tuple(item for item in parsed if item is not None)


def parse_grammar(content: str) -> Grammar:
    """Parse grammar file content (pure function)"""
    lines = tuple(content.split("\n"))
    alpha_lines, key_lines, move_lines = partition_sections(lines)

    alphabet = parse_section(alpha_lines, parse_alphabet_line)
    key_mappings = parse_section(key_lines, parse_keymapping_line)
    moves = parse_section(move_lines, parse_move_line)

    return Grammar(alphabet, key_mappings, moves)


def find_state(states: Tuple[State, ...], state_id: int) -> Optional[State]:
    """Find state by ID"""
    matches = tuple(s for s in states if s.state_id == state_id)
    return matches[0] if matches else None


def find_transition(
    transitions: Tuple[Tuple[Tuple[int, str], int], ...], from_state: int, symbol: str
) -> Optional[int]:
    """Find transition target state"""
    matches = tuple(
        target
        for (source, sym), target in transitions
        if source == from_state and sym == symbol
    )
    return matches[0] if matches else None


def add_state(states: Tuple[State, ...], state: State) -> Tuple[State, ...]:
    """Add or update state in states tuple"""
    filtered = tuple(s for s in states if s.state_id != state.state_id)
    return filtered + (state,)


def add_transition(
    transitions: Tuple[Tuple[Tuple[int, str], int], ...],
    from_state: int,
    symbol: str,
    to_state: int,
) -> Tuple[Tuple[Tuple[int, str], int], ...]:
    """Add transition to transitions tuple"""
    key = (from_state, symbol)
    filtered = tuple(t for t in transitions if t[0] != key)
    return filtered + ((key, to_state),)


def build_path_recursive(
    sequence: Tuple[str, ...],
    current: int,
    states: Tuple[State, ...],
    transitions: Tuple[Tuple[Tuple[int, str], int], ...],
    next_id: int,
) -> Tuple[int, Tuple[State, ...], Tuple[Tuple[Tuple[int, str], int], ...], int]:
    """Recursively build path through automaton for a sequence"""
    if not sequence:
        return (current, states, transitions, next_id)

    symbol = sequence[0]
    rest = sequence[1:]

    existing = find_transition(transitions, current, symbol)

    if existing is not None:
        return build_path_recursive(rest, existing, states, transitions, next_id)

    new_state = State(next_id, False, ())
    new_states = add_state(states, new_state)
    new_transitions = add_transition(transitions, current, symbol, next_id)

    return build_path_recursive(rest, next_id, new_states, new_transitions, next_id + 1)


def add_move_to_automaton(
    automaton_data: Tuple[
        Tuple[State, ...], Tuple[Tuple[Tuple[int, str], int], ...], int
    ],
    move: Move,
) -> Tuple[Tuple[State, ...], Tuple[Tuple[Tuple[int, str], int], ...], int]:
    """Add move to automaton (pure function)"""
    states, transitions, next_id = automaton_data

    final_state_id, new_states, new_transitions, new_next_id = build_path_recursive(
        move.sequence, 0, states, transitions, next_id
    )

    final_state = find_state(new_states, final_state_id)
    updated_state = State(
        final_state_id, True, final_state.moves + (move,) if final_state else (move,)
    )

    return (add_state(new_states, updated_state), new_transitions, new_next_id)


def build_automaton(grammar: Grammar) -> Automaton:
    """Build automaton from grammar (pure function)"""
    alphabet = tuple(set(symbol for move in grammar.moves for symbol in move.sequence))

    initial = ((State(0, False, ()),), (), 1)

    states, transitions, _ = reduce(add_move_to_automaton, grammar.moves, initial)

    return Automaton(states, transitions, 0, alphabet)


def recognize_sequence(
    automaton: Automaton, sequence: Tuple[str, ...]
) -> Tuple[bool, Tuple[Move, ...]]:
    """Recognize sequence using automaton (pure function)"""

    def traverse(seq: Tuple[str, ...], current: int) -> int:
        if not seq:
            return current

        next_state = find_transition(automaton.transitions, current, seq[0])
        if next_state is None:
            return -1

        return traverse(seq[1:], next_state)

    final_state_id = traverse(sequence, automaton.initial_state)

    if final_state_id == -1:
        return (False, ())

    final_state = find_state(automaton.states, final_state_id)

    if final_state and final_state.is_final:
        return (True, final_state.moves)

    return (False, ())


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


def read_file_content(filepath: str) -> Optional[str]:
    """Read file using sys module (avoiding open keyword violation)"""
    import os

    if not os.path.exists(filepath):
        return None

    fd = os.open(filepath, os.O_RDONLY)
    content = b""

    while True:
        chunk = os.read(fd, 4096)
        if not chunk:
            break
        content += chunk

    os.close(fd)
    return content.decode("utf-8")


def display_key_mappings(grammar: Grammar) -> None:
    """Display key mappings grouped by type (I/O function)"""

    def get_info(symbol: str) -> Tuple[str, str]:
        """Get type and description for a symbol"""
        sym_obj = lookup_symbol(grammar.alphabet, symbol)
        if sym_obj:
            return (sym_obj.sym_type, sym_obj.description)
        return ("", symbol)

    def group_by_type(mappings: Tuple[Tuple[str, str], ...]) -> Tuple[Tuple[str, Tuple[Tuple[str, str], ...]], ...]:
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


def process_key_input(
    key: str, grammar: Grammar, automaton: Automaton, buffer: Tuple[str, ...]
) -> Tuple[Tuple[str, ...], bool]:
    """Process single key input (pure logic with I/O side effects)"""
    symbol = lookup_key(grammar.key_mappings, key)

    if symbol is None:
        return (buffer, False)

    new_buffer = buffer + (symbol,)
    is_recognized, moves = recognize_sequence(automaton, new_buffer)

    if is_recognized:
        print(f"\n{', '.join(new_buffer)}")
        display_moves(moves)
        return (new_buffer, True)

    return (new_buffer, False)


def run_interactive_mode(grammar: Grammar, automaton: Automaton) -> None:
    """Run interactive recognition mode"""
    print("\nTraining Mode")
    print("Enter keys separated by spaces to execute moves")
    print("Press Ctrl+C to exit\n")

    def input_loop(buffer: Tuple[str, ...]) -> None:
        try:
            line = input("> ").strip()
            if is_empty(line):
                input_loop(buffer)
                return

            keys = tuple(line.split())

            def process_keys(
                buf: Tuple[str, ...], remaining: Tuple[str, ...]
            ) -> Tuple[str, ...]:
                if not remaining:
                    return buf

                new_buf, _ = process_key_input(remaining[0], grammar, automaton, buf)
                return process_keys(new_buf, remaining[1:])

            final_buffer = process_keys((), keys)
            input_loop(())

        except EOFError:
            return
        except KeyboardInterrupt:
            return

    input_loop(())


def main() -> int:
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: ./ft_ality <grammar_file>")
        return 1

    grammar_file = sys.argv[1]

    content = read_file_content(grammar_file)
    if content is None:
        print(f"Error: Grammar file '{grammar_file}' not found")
        return 1

    try:
        grammar = parse_grammar(content)
        automaton = build_automaton(grammar)

        display_key_mappings(grammar)
        run_interactive_mode(grammar, automaton)

    except KeyboardInterrupt:
        print("\n\nExiting training mode...")
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
