"""ft_ality - Main entry point"""

import sys
from src import (
    parse_grammar,
    build_automaton,
    display_key_mappings,
    run_interactive_mode,
    read_file_content,
)


def _run(grammar_file: str, debug: bool) -> int:
    """Parse grammar, build automaton, and enter interactive mode."""
    content = read_file_content(grammar_file)
    if content is None:
        print(f"Error: Grammar file '{grammar_file}' not found")
        return 1
    grammar = parse_grammar(content)
    automaton = build_automaton(grammar)
    display_key_mappings(grammar)
    run_interactive_mode(grammar, automaton, debug)
    return 0


def main() -> int:
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: ./ft_ality <grammar_file> [--debug]")
        return 1
    return _run(sys.argv[1], "--debug" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
