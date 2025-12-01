# Advent of Code 2025

Solutions for [Advent of Code 2025](https://adventofcode.com/2025) in Python.

## Project Structure

```
advent-of-code-2025/
├── aoc2025.py              # Main entry point
├── internal/
│   ├── days/
│   │   ├── day01/
│   │   │   ├── day01.py       # Solution implementation
│   │   │   ├── day01_test.py  # Tests
│   │   │   └── input.py       # Puzzle input constants
│   │   └── ...
│   └── utils/
│       ├── parsing.py      # Parsing utilities
│       └── ...
├── requirements.txt
└── README.md
```

This structure mirrors the [2024 Go project](https://github.com/amoilanen/advent-of-code-2024) layout.

## Running Solutions

Run all days:
```bash
python aoc2025.py
```

Run a specific day:
```bash
python aoc2025.py 1
# or
python aoc2025.py day01
```

## Running Tests

With pytest:
```bash
# All tests
python -m pytest

# Specific day
python -m pytest internal/days/day01/day01_test.py -v

# With coverage
python -m pytest --cov=internal
```

## Adding Your Input

1. Go to [Advent of Code 2025](https://adventofcode.com/2025)
2. Log in and navigate to the day's puzzle
3. Copy your puzzle input
4. Paste it into `internal/days/dayXX/input.py` replacing the `DAY_INPUT` constant

Example:
```python
DAY_INPUT = """L68
L30
R48
..."""
```

## Requirements

- Python 3.10+ (for modern type hints)
- pytest (optional, for running tests)

To install dependencies:
```bash
pip install -r requirements.txt
```
