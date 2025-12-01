"""Parsing utilities for Advent of Code solutions"""


def as_lines(input_text: str) -> list[str]:
    """Split input into lines and strip whitespace from each line."""
    return [line.strip() for line in input_text.strip().split('\n')]


def parse_ints(input_text: str) -> list[int]:
    """Parse space-separated integers from a string."""
    return [int(x) for x in input_text.split()]


def parse_int(s: str) -> int:
    """Parse a single integer, stripping whitespace."""
    return int(s.strip())
