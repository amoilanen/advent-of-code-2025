"""Day 5: Fresh Ingredient Database

Determine which ingredient IDs are fresh based on fresh ID ranges.
"""
from dataclasses import dataclass

@dataclass
class PuzzleInput:
    ranges: list[tuple[int, int]]
    ingredient_ids: list[int]

def parse(input_text: str) -> PuzzleInput:
    """
    Parse the input into fresh ingredient ranges and available ingredient IDs.

    Args:
        input_text: The puzzle input containing ranges and ingredient IDs

    Returns:
        A tuple of (ranges, ingredient_ids) where:
        - ranges is a list of (start, end) tuples representing fresh ID ranges
        - ingredient_ids is a list of available ingredient IDs to check
    """
    if not input_text.strip():
        return ([], [])

    # Split by blank line, but don't strip first to preserve structure
    parts = input_text.split('\n\n')

    # Parse ranges from first part
    ranges = []
    if len(parts) > 0 and parts[0].strip():
        for line in parts[0].strip().split('\n'):
            if '-' in line:
                start, end = line.split('-')
                ranges.append((int(start), int(end)))

    # Parse ingredient IDs from second part
    ingredient_ids = []
    if len(parts) > 1 and parts[1].strip():
        for line in parts[1].strip().split('\n'):
            ingredient_ids.append(int(line))

    return PuzzleInput(ranges, ingredient_ids)


def is_fresh(ingredient_id: int, ranges: list[tuple[int, int]]) -> bool:
    """
    Check if an ingredient ID is fresh (falls within any range).

    Args:
        ingredient_id: The ingredient ID to check
        ranges: List of (start, end) tuples representing fresh ID ranges

    Returns:
        True if the ingredient is fresh, False otherwise
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ingredients(ranges: list[tuple[int, int]], ingredient_ids: list[int]) -> int:
    """
    Count how many of the available ingredient IDs are fresh.

    Args:
        ranges: List of (start, end) tuples representing fresh ID ranges
        ingredient_ids: List of available ingredient IDs to check

    Returns:
        Number of fresh ingredients
    """
    return sum(1 for ingredient_id in ingredient_ids if is_fresh(ingredient_id, ranges))


def part1(input: PuzzleInput) -> int:
    """
    Solve part 1: Count how many available ingredient IDs are fresh.

    Args:
        ranges: List of (start, end) tuples representing fresh ID ranges
        ingredient_ids: List of available ingredient IDs to check

    Returns:
        Number of fresh ingredients
    """
    return count_fresh_ingredients(input.ranges, input.ingredient_ids)

def part2(input: PuzzleInput) -> int:
    # TODO: Implement
    return 0
