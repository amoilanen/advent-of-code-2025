"""Day 1: Safe Dial Combination

The safe has a dial with numbers 0-99 that starts at 50.
Given a sequence of rotations (L for left/lower, R for right/higher),
count how many times the dial points to 0 after any rotation.
"""


def parse(input_text: str) -> list[tuple[str, int]]:
    """Parse the input into a list of (direction, distance) tuples."""
    rotations = []
    for line in input_text.strip().split('\n'):
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def part1(rotations: list[tuple[str, int]]) -> int:
    """
    Calculate the password by counting how many times the dial points at 0
    after any rotation in the sequence.

    The dial starts at 50 and has numbers 0-99 in a circle.
    L means rotate left (toward lower numbers), R means rotate right (toward higher numbers).
    """
    position = 50
    count_zeros = 0

    for direction, distance in rotations:
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100

        if position == 0:
            count_zeros += 1

    return count_zeros


def part2(rotations: list[tuple[str, int]]) -> int:
    """Part 2 solution (to be implemented when puzzle is unlocked)."""
    return 0
