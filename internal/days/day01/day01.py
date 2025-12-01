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
    """
    Calculate the password by counting how many times the dial points at 0
    during ANY click in the rotation sequence (method 0x434C49434B).

    This counts every time the dial passes through 0 during a rotation,
    not just when it ends at 0.
    """
    import math

    position = 50
    count_zeros = 0

    for direction, distance in rotations:
        # Count how many times we pass through 0 during this rotation
        if direction == 'L':
            # For left rotation, we pass through 0 when moving from pos to pos-dist
            # We pass through 0 at steps where (pos - k) ≡ 0 (mod 100)
            # This happens when k = pos - 100*m for integer m
            # Valid k must be in range [1, distance]
            m_min = math.ceil((position - distance) / 100)
            m_max = (position - 1) // 100
            count = max(0, m_max - m_min + 1)
        else:  # direction == 'R'
            # For right rotation, we pass through 0 when moving from pos to pos+dist
            # We pass through 0 at steps where (pos + k) ≡ 0 (mod 100)
            # This happens when k = 100*m - pos for positive integer m
            # Valid k must be in range [1, distance]
            count = (position + distance) // 100

        count_zeros += count

        # Update position
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

    return count_zeros
