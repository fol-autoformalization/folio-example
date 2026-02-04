#!/usr/bin/env python3
"""
Basic FOLIO parser using Lark
Converts educational FOL syntax to parse trees
"""

from lark import Lark, Tree
from pathlib import Path


class FOLIOParser:
    def __init__(self, grammar_file="folio_grammar.lark"):
        grammar_path = Path(__file__).parent / grammar_file
        with open(grammar_path) as f:
            self.parser = Lark(f.read(), start='start', parser='lalr')

    def parse(self, formula: str) -> Tree:
        """Parse a FOLIO formula into a parse tree"""
        return self.parser.parse(formula)

    def parse_file(self, jsonl_file: str):
        """Parse formulas from a FOLIO JSONL file"""
        import json
        results = []

        with open(jsonl_file) as f:
            for line in f:
                data = json.loads(line)
                story_id = data['story_id']

                try:
                    # Parse premises
                    premises_trees = []
                    for premise in data['premises-FOL'].strip().split('\n'):
                        if premise.strip():
                            tree = self.parse(premise)
                            premises_trees.append(tree)

                    # Parse conclusion
                    conclusion_tree = self.parse(data['conclusion-FOL'])

                    results.append({
                        'story_id': story_id,
                        'premises': premises_trees,
                        'conclusion': conclusion_tree,
                        'label': data['label']
                    })
                except Exception as e:
                    print(f"Error parsing story {story_id}: {e}")
                    results.append({
                        'story_id': story_id,
                        'error': str(e)
                    })

        return results


if __name__ == "__main__":
    parser = FOLIOParser()

    # Test on a few simple formulas
    test_formulas = [
        "Student(rina)",
        "∀x (Student(x) → Smart(x))",
        "Student(rina) ∧ Smart(rina)",
        "∃x (Student(x) ∧ Smart(x))",
    ]

    print("Testing basic formulas:\n")
    for formula in test_formulas:
        try:
            tree = parser.parse(formula)
            print(f"✓ {formula}")
            print(f"  {tree.pretty()}\n")
        except Exception as e:
            print(f"✗ {formula}")
            print(f"  Error: {e}\n")
