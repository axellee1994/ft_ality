"""ft_ality - Finite-State Automaton for fighting game move recognition"""

import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <grammar_file>")
        sys.exit(1)

    grammar_file = sys.argv[1]

    try:
        with open(grammar_file, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"Error: Grammar file '{grammar_file}' not found")
        sys.exit(1)
