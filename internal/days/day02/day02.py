"""Day 2: Invalid Product IDs

Find invalid product IDs in given ranges. An invalid ID is one that consists
of some sequence of digits repeated exactly twice (e.g., 11, 6464, 123123).
"""

def parse(input_text: str) -> list[tuple[int, int]]:
    """Parse the input into a list of (start, end) range tuples."""
    ranges = []
    for range_str in input_text.strip().split(','):
        if not range_str:
            continue
        start_str, end_str = range_str.split('-')
        ranges.append((int(start_str), int(end_str)))
    return ranges

def is_invalid_id(num: int) -> bool:
    """
    Check if a number is an invalid ID.

    An invalid ID is made only of some sequence of digits repeated twice.
    For example: 11 (1 twice), 6464 (64 twice), 123123 (123 twice).

    Numbers with leading zeros (like 0101) are not valid IDs at all.
    """
    s = str(num)
    length = len(s)

    # Must have even length to split in half
    if length % 2 != 0:
        return False

    # Split in half and check if both halves are identical
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]

    return first_half == second_half

def is_invalid_id_part2(num: int) -> bool:
    """
    Check if a number is an invalid ID for Part 2.

    An invalid ID is made of some sequence of digits repeated at least twice.
    For example: 11 (1 twice), 111 (1 three times), 6464 (64 twice),
    123123123 (123 three times), 1212121212 (12 five times).

    Algorithm: Check if the number can be formed by repeating a pattern.
    For a number of length n, try all divisors d of n where d < n.
    If the first d characters repeated n/d times equals the full string, it's invalid.
    """
    s = str(num)
    n = len(s)

    # Single digit cannot be repeated at least twice
    if n == 1:
        return False

    # Try all possible pattern lengths (divisors of n)
    for pattern_len in range(1, n // 2 + 1):
        if n % pattern_len == 0:
            # Check if repeating the pattern creates the full number
            pattern = s[:pattern_len]
            repetitions = n // pattern_len
            if pattern * repetitions == s:
                return True

    return False


def _sum_invalid_ids(ranges: list[tuple[int, int]], validator) -> int:
    """
    Helper function to find all invalid IDs in ranges and sum them.

    Args:
        ranges: List of (start, end) range tuples
        validator: Function to check if a number is invalid

    Returns:
        Sum of all invalid IDs
    """
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if validator(num):
                total += num

    return total


def part1(ranges: list[tuple[int, int]]) -> int:
    """
    Find all invalid IDs in the given ranges and sum them.

    For each range (start, end), check every ID in that range.
    If it's invalid (repeated exactly twice), add it to the sum.
    """
    return _sum_invalid_ids(ranges, is_invalid_id)


def part2(ranges: list[tuple[int, int]]) -> int:
    """
    Find all invalid IDs in the given ranges and sum them (Part 2 rules).

    For each range (start, end), check every ID in that range.
    If it's invalid (repeated pattern at least twice), add it to the sum.
    """
    return _sum_invalid_ids(ranges, is_invalid_id_part2)
