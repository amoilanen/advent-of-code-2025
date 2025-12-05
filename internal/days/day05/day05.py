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
        return PuzzleInput([], [])

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


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping and adjacent ranges into a minimal set of non-overlapping ranges.

    Algorithm:
    1. Sort ranges by start position
    2. Merge overlapping/adjacent ranges
    3. Ranges [a, b] and [c, d] can merge if c <= b + 1

    Args:
        ranges: List of (start, end) tuples

    Returns:
        List of merged (start, end) tuples with no overlaps
    """
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    # Initialize with first range
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if current range overlaps or is adjacent to the last merged range
        if start <= last_end + 1:
            # Merge: extend the last range to cover both
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap: add as new range
            merged.append((start, end))

    return merged


def count_total_fresh_ids(ranges: list[tuple[int, int]]) -> int:
    """
    Count the total number of unique ingredient IDs covered by all ranges.

    Uses range merging to efficiently handle overlapping ranges.

    Args:
        ranges: List of (start, end) tuples representing fresh ID ranges

    Returns:
        Total number of unique fresh ingredient IDs
    """
    merged = merge_ranges(ranges)

    # Sum up the sizes of all merged ranges
    total = 0
    for start, end in merged:
        total += end - start + 1  # +1 because ranges are inclusive

    return total


def part1(input: PuzzleInput) -> int:
    """
    Solve part 1: Count how many available ingredient IDs are fresh.

    Args:
        input: Parsed puzzle input with ranges and ingredient IDs

    Returns:
        Number of fresh ingredients from the available list
    """
    return count_fresh_ingredients(input.ranges, input.ingredient_ids)


def part2(input: PuzzleInput) -> int:
    """
    Solve part 2: Count total number of ingredient IDs considered fresh by the ranges.

    Args:
        input: Parsed puzzle input with ranges and ingredient IDs

    Returns:
        Total number of unique fresh ingredient IDs across all ranges
    """
    return count_total_fresh_ids(input.ranges)
