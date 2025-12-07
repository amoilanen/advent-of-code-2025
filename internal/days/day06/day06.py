"""Day 6: Cephalopod Math Worksheet

Solve vertically-arranged math problems from a worksheet.
"""
from dataclasses import dataclass
from functools import reduce
import operator


@dataclass
class Problem:
    """Represents a single math problem."""
    numbers: list[int]
    operation: str


@dataclass
class PuzzleInput:
    """Represents the parsed worksheet."""
    problems: list[Problem]


def pad_lines(lines: list[str]) -> list[str]:
    """
    Pad all lines to the same width with spaces.

    Args:
        lines: List of text lines

    Returns:
        List of lines padded to same width
    """
    if not lines:
        return []
    max_width = max(len(line) for line in lines)
    return [line.ljust(max_width) for line in lines]


def extract_number_from_string(s: str, strip_operation: bool = False) -> int | None:
    """
    Extract a number from a string, optionally removing operation symbol.

    Args:
        s: String containing digits and possibly spaces/operation
        strip_operation: If True, remove trailing operation symbol before parsing

    Returns:
        Parsed integer, or None if no valid number found
    """
    if strip_operation:
        s = s.rstrip()
        if s and s[-1] in ['+', '*']:
            s = s[:-1]

    number_str = s.replace(' ', '')
    return int(number_str) if number_str else None


def create_problem_if_valid(numbers: list[int], operation: str | None) -> Problem | None:
    """
    Create a Problem if both numbers and operation are valid.

    Args:
        numbers: List of numbers in the problem
        operation: Operation symbol ('+' or '*')

    Returns:
        Problem instance, or None if invalid
    """
    if numbers and operation:
        return Problem(numbers, operation)
    return None


def transpose_grid(lines: list[str]) -> list[str]:
    """
    Transpose a grid of text (convert columns to rows).

    Args:
        lines: List of text lines

    Returns:
        Transposed lines (columns become rows)
    """
    padded_lines = pad_lines(lines)
    if not padded_lines:
        return []

    max_width = len(padded_lines[0])
    col_range = range(max_width)

    transposed = []
    for col_idx in col_range:
        row = ''.join(padded_lines[row_idx][col_idx] for row_idx in range(len(padded_lines)))
        transposed.append(row)

    return transposed


def parse_from_columns(lines: list[str]) -> PuzzleInput:
    """
    Parse problems from columns (used for Part 1 normal reading).

    Problems are separated by empty columns.
    Within each problem:
    - Each row (except last) represents one number, read left-to-right
    - The last row contains the operation

    Args:
        lines: List of text lines

    Returns:
        PuzzleInput with list of problems
    """
    padded_lines = pad_lines(lines)
    if not padded_lines:
        return PuzzleInput([])

    max_width = len(padded_lines[0])

    # Group columns into problems (separated by fully empty columns)
    problem_column_groups = []
    current_problem_cols = []

    for col_idx in range(max_width):
        # Check if column is completely empty
        column_chars = [padded_lines[row][col_idx] for row in range(len(padded_lines))]
        is_empty = all(c == ' ' for c in column_chars)

        if not is_empty:
            current_problem_cols.append(col_idx)
        else:
            if current_problem_cols:
                problem_column_groups.append(current_problem_cols)
                current_problem_cols = []

    if current_problem_cols:
        problem_column_groups.append(current_problem_cols)

    # Parse each problem
    problems = []
    for prob_cols in problem_column_groups:
        # Extract the operation from the last row
        operation = None
        for col_idx in prob_cols:
            char = padded_lines[-1][col_idx]
            if char in ['+', '*']:
                operation = char
                break

        # Extract numbers from each row (except last which has operation)
        numbers = []
        for row_idx in range(len(padded_lines) - 1):
            # Get the substring for this problem in this row
            row_str = ''.join(padded_lines[row_idx][col_idx] for col_idx in prob_cols)
            number = extract_number_from_string(row_str)
            if number is not None:
                numbers.append(number)

        problem = create_problem_if_valid(numbers, operation)
        if problem:
            problems.append(problem)

    return PuzzleInput(problems)


def parse_from_rows(lines: list[str]) -> PuzzleInput:
    """
    Parse problems from rows (used after transposing for cephalopod reading).

    Each row represents one number, with the operation at the end of the last row.
    Empty rows separate problems.

    Args:
        lines: List of text lines (rows after transposing)

    Returns:
        PuzzleInput with list of problems
    """
    if not lines:
        return PuzzleInput([])

    problems = []
    current_numbers = []
    current_operation = None

    for line in lines:
        # Check if this is an empty line (problem separator)
        if not line.strip():
            problem = create_problem_if_valid(current_numbers, current_operation)
            if problem:
                problems.append(problem)
            current_numbers = []
            current_operation = None
            continue

        # Check if last character is an operation
        last_char = line.rstrip()[-1] if line.rstrip() else ' '

        if last_char in ['+', '*']:
            current_operation = last_char
            number = extract_number_from_string(line, strip_operation=True)
        else:
            number = extract_number_from_string(line)

        if number is not None:
            current_numbers.append(number)

    # Don't forget the last problem
    problem = create_problem_if_valid(current_numbers, current_operation)
    if problem:
        problems.append(problem)

    return PuzzleInput(problems)


def parse_part1(input_text: str) -> PuzzleInput:
    """
    Parse the worksheet for Part 1 (normal left-to-right reading).

    Parse column-based problems directly.

    Args:
        input_text: The worksheet text

    Returns:
        PuzzleInput with list of problems
    """
    lines = input_text.strip().split('\n')
    return parse_from_columns(lines)


def evaluate_problem(problem: Problem) -> int:
    """
    Evaluate a single math problem.

    Args:
        problem: The problem to evaluate

    Returns:
        The result of the calculation
    """
    if not problem.numbers:
        return 0

    if problem.operation == '+':
        return sum(problem.numbers)
    elif problem.operation == '*':
        return reduce(operator.mul, problem.numbers, 1)
    else:
        raise ValueError(f"Unknown operation: {problem.operation}")


def solve_worksheet(problems: list[Problem]) -> int:
    """
    Solve all problems and return the grand total.

    Args:
        problems: List of problems to solve

    Returns:
        Sum of all problem results
    """
    return sum(evaluate_problem(problem) for problem in problems)


def part1(input: PuzzleInput) -> int:
    """
    Solve part 1: Calculate the grand total of all problems.

    Args:
        input: Parsed worksheet input

    Returns:
        Grand total
    """
    return solve_worksheet(input.problems)


def parse_part2(input_text: str) -> PuzzleInput:
    """
    Parse the math worksheet using cephalopod reading (right-to-left).

    Transpose columns to rows (right-to-left), then parse rows.

    Args:
        input_text: The worksheet text

    Returns:
        PuzzleInput with list of problems
    """
    lines = input_text.strip().split('\n')
    transposed = transpose_grid(lines)
    return parse_from_rows(transposed)


def part2(input: PuzzleInput) -> int:
    """
    Solve part 2: Calculate grand total using cephalopod reading.

    Args:
        input: Parsed worksheet input (using cephalopod reading)

    Returns:
        Grand total
    """
    return solve_worksheet(input.problems)
