"""Day 3: Battery Joltage

Find the maximum joltage from battery banks by selecting exactly two batteries
from each bank to maximize the two-digit number formed.
"""


def parse(input_text: str) -> list[str]:
    """
    Parse the input into a list of battery banks.

    Each non-empty line is a bank of batteries.
    """
    banks = []
    for line in input_text.strip().split('\n'):
        if line:
            banks.append(line)
    return banks

def max_joltage(bank: str) -> int:
    return max_joltage_n(bank, 2)

def max_joltage_n(bank: str, n: int) -> int:
    """
    Find the maximum joltage possible by selecting exactly n batteries from a bank.

    Uses a greedy algorithm: for each position in the result, select the largest
    digit from the remaining bank such that we still have enough digits left to
    complete the selection.

    Algorithm:
    1. Start with an empty result and the full bank
    2. For each of the n positions we need to fill:
       - Calculate how many more digits we need after this one (remaining = n - len(result) - 1)
       - We can only consider digits from indices 0 to (len(bank) - remaining - 1)
       - Find the maximum digit in that range
       - Add it to result and remove everything up to and including that digit from bank

    Args:
        bank: String of digits representing battery joltage ratings
        n: Number of batteries to select

    Returns:
        Maximum n-digit joltage possible from the bank

    Example:
        bank="987654321111111", n=12
        - Need 12 digits total (15 available, skip 3)
        - Position 1: Can check indices 0-3, max is '9' at 0. Result="9", bank="87654321111111"
        - Position 2: Can check indices 0-4, max is '8' at 0. Result="98", bank="7654321111111"
        - Continue until we have 12 digits
    """
    if len(bank) < n:
        raise ValueError(f"Bank must have at least {n} batteries")

    if len(bank) == n:
        return int(bank)

    result = []
    current_pos = 0  # Current position in the original bank

    for position in range(n):
        # How many more digits do we need after the next digit we are going to select?
        remaining_needed = n - position - 1

        # We can search up to this index (inclusive)
        # We need to leave enough digits for the remaining positions
        max_search_pos = len(bank) - remaining_needed

        # Find the maximum digit in the valid range
        max_digit = bank[current_pos]
        max_digit_pos = current_pos

        for i in range(current_pos, max_search_pos):
            if bank[i] > max_digit:
                max_digit = bank[i]
                max_digit_pos = i

        # Add the selected digit to result
        result.append(max_digit)
        # Move past the selected digit
        current_pos = max_digit_pos + 1

    return int(''.join(result))


def part1(banks: list[str]) -> int:
    """
    Calculate the total output joltage from all battery banks.

    For each bank, find the maximum joltage possible and sum them all.
    """
    return sum(max_joltage_n(bank, 2) for bank in banks)


def part2(banks: list[str]) -> int:
    """
    Calculate the total output joltage from all battery banks (Part 2).

    For each bank, find the maximum joltage possible by selecting exactly
    12 batteries, then sum them all.
    """
    return sum(max_joltage_n(bank, 12) for bank in banks)
