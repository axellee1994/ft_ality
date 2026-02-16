"""ft_ality - Main entry point"""

import sys
from src import (
    parse_grammar,
    build_automaton,
    display_key_mappings,
    run_interactive_mode,
    read_file_content,
)


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
