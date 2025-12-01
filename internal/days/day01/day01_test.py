"""Tests for Day 1 solution"""

import pytest
from .day01 import parse, part1, part2
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        rotations = parse(EXAMPLE_INPUT)
        expected = [
            ('L', 68), ('L', 30), ('R', 48), ('L', 5), ('R', 60),
            ('L', 55), ('L', 1), ('L', 99), ('R', 14), ('L', 82)
        ]
        assert rotations == expected

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        rotations = parse("")
        assert rotations == []

    def test_parse_single_line(self):
        """Test parsing a single rotation."""
        rotations = parse("R10")
        assert rotations == [('R', 10)]

    def test_parse_various_formats(self):
        """Test parsing various rotation formats."""
        rotations = parse("L1\nR99\nL0\nR50")
        assert rotations == [('L', 1), ('R', 99), ('L', 0), ('R', 50)]


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        rotations = parse(EXAMPLE_INPUT)
        assert part1(rotations) == 3

    def test_no_zeros(self):
        """Test case where dial never points to 0."""
        rotations = [('R', 10), ('L', 5)]  # 50 -> 60 -> 55
        assert part1(rotations) == 0

    def test_immediate_zero(self):
        """Test when first rotation points to 0."""
        rotations = [('L', 50)]  # 50 -> 0
        assert part1(rotations) == 1

    def test_multiple_zeros(self):
        """Test case with multiple zeros."""
        rotations = [
            ('L', 50),  # 50 -> 0 (count: 1)
            ('R', 100), # 0 -> 0 (count: 2)
            ('L', 0),   # 0 -> 0 (count: 3)
            ('R', 50),  # 0 -> 50
            ('L', 50),  # 50 -> 0 (count: 4)
        ]
        assert part1(rotations) == 4

    def test_wrap_around_right(self):
        """Test wrapping around when rotating right."""
        rotations = [('R', 51)]  # 50 + 51 = 101 -> 1
        assert part1(rotations) == 0

    def test_wrap_around_left(self):
        """Test wrapping around when rotating left."""
        rotations = [('L', 51)]  # 50 - 51 = -1 -> 99
        assert part1(rotations) == 0

    def test_exact_wrap_to_zero(self):
        """Test exact wrap to 0."""
        rotations = [('R', 50)]  # 50 + 50 = 100 -> 0
        assert part1(rotations) == 1


class TestPart2:
    def test_example(self):
        """Test with the example from problem description for part 2."""
        rotations = parse(EXAMPLE_INPUT)
        assert part2(rotations) == 6

    def test_multiple_passes(self):
        """Test R1000 from position 50 passes through 0 ten times."""
        rotations = [('R', 1000)]
        assert part2(rotations) == 10

    def test_no_passes(self):
        """Test rotation that doesn't pass through 0."""
        rotations = [('R', 10)]  # 50 -> 60, no crossing
        assert part2(rotations) == 0

    def test_single_pass_right(self):
        """Test right rotation passing through 0 once."""
        rotations = [('R', 50)]  # 50 -> 0, passes through 0 at step 50
        assert part2(rotations) == 1

    def test_single_pass_left(self):
        """Test left rotation passing through 0 once."""
        rotations = [('L', 68)]  # 50 -> 82, passes through 0 during rotation
        assert part2(rotations) == 1


def test_manual_walk_through():
    """Manually walk through the example to verify logic."""
    rotations = [
        ('L', 68),  # 50 - 68 = -18 -> 82
        ('L', 30),  # 82 - 30 = 52
        ('R', 48),  # 52 + 48 = 100 -> 0 ✓
        ('L', 5),   # 0 - 5 = -5 -> 95
        ('R', 60),  # 95 + 60 = 155 -> 55
        ('L', 55),  # 55 - 55 = 0 ✓
        ('L', 1),   # 0 - 1 = -1 -> 99
        ('L', 99),  # 99 - 99 = 0 ✓
        ('R', 14),  # 0 + 14 = 14
        ('L', 82),  # 14 - 82 = -68 -> 32
    ]

    position = 50
    positions = [position]

    for direction, distance in rotations:
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        positions.append(position)

    expected_positions = [50, 82, 52, 0, 95, 55, 0, 99, 0, 14, 32]
    assert positions == expected_positions

    zeros_count = sum(1 for p in positions[1:] if p == 0)
    assert zeros_count == 3
