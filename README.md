# FOLIO Parser - Minimal Example

Simple example showing how to parse FOLIO dataset formulas.

## Files

- `folio_grammar.lark` - Lark grammar for FOLIO FOL syntax
- `parser.py` - Parser class
- `example_usage.py` - Usage examples with HuggingFace dataset
- `.env` - HuggingFace token (add your own)

## Setup

```bash
# Install dependencies
pip install lark datasets huggingface-hub python-dotenv

# Add HuggingFace token
echo "HF_TOKEN=your_token_here" > .env

# Run example
python example_usage.py
```

## Usage

```python
from parser import FOLIOParser

parser = FOLIOParser()
tree = parser.parse("∀x (Student(x) → Smart(x))")
print(tree.pretty())
```

## What It Does

1. Loads FOLIO dataset from HuggingFace
2. Parses formulas into syntax trees
3. Shows parse success rate (97.1% on valid formulas)
4. Demonstrates error handling

## Output

```
Loading FOLIO dataset from HuggingFace...
Dataset loaded

Example 1: First training example
Story ID: 406
Parsing premises: 5 OK
Parsing conclusion: OK
Label: True

Example 4: Count valid formulas
First 50 stories:
  Valid formulas: 300
  Invalid formulas: 9
  Success rate: 97.1%
```
