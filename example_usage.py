#!/usr/bin/env python3
"""
Simple example showing how to use the FOLIO parser

Run with: python example_usage.py
"""

import os
from parser import FOLIOParser
from datasets import load_dataset

# Initialize parser
parser = FOLIOParser()

# Load FOLIO dataset from HuggingFace
print("Loading FOLIO dataset from HuggingFace...")
token = os.getenv('HF_TOKEN')
dataset = load_dataset("tasksource/folio", token=token)

print("Dataset loaded")
print()

# Example 1: Parse first training example
print("-" * 70)
print("Example 1: First training example")
print("-" * 70)

example = dataset['train'][0]
print("Story ID:", example['story_id'])
print()

# Parse all premises
premises = example['premises-FOL'].strip().split('\n')
print("Parsing premises:")
for i, premise in enumerate(premises, 1):
    try:
        tree = parser.parse(premise)
        print(f"  Premise {i}: OK")
    except Exception as e:
        print(f"  Premise {i}: ERROR - {str(e)[:50]}")

# Parse conclusion
print()
print("Parsing conclusion:")
try:
    tree = parser.parse(example['conclusion-FOL'])
    print("  Conclusion: OK")
except Exception as e:
    print(f"  Conclusion: ERROR - {str(e)[:50]}")

print()
print("Label:", example['label'])
print()

# Example 2: Parse a few more examples
print("-" * 70)
print("Example 2: Parse multiple examples")
print("-" * 70)

for i in range(3):
    example = dataset['train'][i]
    premises = example['premises-FOL'].strip().split('\n')

    premises_ok = 0
    premises_fail = 0

    for premise in premises:
        if premise.strip():
            try:
                parser.parse(premise)
                premises_ok += 1
            except:
                premises_fail += 1

    try:
        parser.parse(example['conclusion-FOL'])
        conclusion_ok = True
    except:
        conclusion_ok = False

    print(f"Story {example['story_id']}: {premises_ok} premises OK, {premises_fail} failed, conclusion {'OK' if conclusion_ok else 'FAIL'}")

print()

# Example 3: Show a parsed formula structure
print("-" * 70)
print("Example 3: Examine parse tree structure")
print("-" * 70)

formula = dataset['train'][0]['premises-FOL'].strip().split('\n')[0]
print("Formula:", formula)
print()

tree = parser.parse(formula)
print("Parse tree (abbreviated):")
print(tree.pretty()[:500])
print("...")
print()

# Example 4: Count valid formulas in dataset
print("-" * 70)
print("Example 4: Count valid formulas")
print("-" * 70)

valid_count = 0
invalid_count = 0

for i in range(50):
    example = dataset['train'][i]
    premises = example['premises-FOL'].strip().split('\n')

    for premise in premises:
        if premise.strip():
            try:
                parser.parse(premise)
                valid_count += 1
            except:
                invalid_count += 1

    try:
        parser.parse(example['conclusion-FOL'])
        valid_count += 1
    except:
        invalid_count += 1

total = valid_count + invalid_count
success_rate = 100 * valid_count / total if total > 0 else 0

print(f"First 50 stories:")
print(f"  Valid formulas: {valid_count}")
print(f"  Invalid formulas: {invalid_count}")
print(f"  Success rate: {success_rate:.1f}%")
