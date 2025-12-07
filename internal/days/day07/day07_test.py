"""Tests for Day 7 solution"""

import pytest
from .day07 import parse, part1, part2
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        grid, start_row, start_col = parse(EXAMPLE_INPUT)
        assert len(grid) == 16
        assert start_row == 0
        assert start_col == 7
        assert grid[0][7] == 'S'
        assert grid[2][7] == '^'

    def test_parse_simple(self):
        """Test parsing a simple grid."""
        input_text = """S.
.^"""
        grid, start_row, start_col = parse(input_text)
        assert len(grid) == 2
        assert start_row == 0
        assert start_col == 0
        assert grid[0][0] == 'S'
        assert grid[1][1] == '^'


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        grid, start_row, start_col = parse(EXAMPLE_INPUT)
        assert part1(grid, start_row, start_col) == 21

    def test_no_splitters(self):
        """Test with no splitters."""
        input_text = """S.
.."""
        grid, start_row, start_col = parse(input_text)
        assert part1(grid, start_row, start_col) == 0

    def test_beam_exits_bounds(self):
        """Test when beam exits bounds."""
        input_text = """S.
.."""
        grid, start_row, start_col = parse(input_text)
        assert part1(grid, start_row, start_col) == 0

    def test_multiple_splitters_in_line_none_encountered(self):
        """Test with multiple splitters in a line."""
        input_text = """S.
.^
.^"""
        grid, start_row, start_col = parse(input_text)
        # Beam moves down from S at (0,0) to (1,0), then exits
        # Splitters are at (1,1) and (2,1), so beam never hits them
        assert part1(grid, start_row, start_col) == 0
    
    def test_splitter_directly_below(self):
        """Test with splitter directly below S."""
        input_text = """S
^"""
        grid, start_row, start_col = parse(input_text)
        # Beam moves down from S at (0,0) to (1,0) which is a splitter
        # Total: 1 split
        assert part1(grid, start_row, start_col) == 1


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        grid, start_row, start_col = parse(EXAMPLE_INPUT)
        assert part2(grid, start_row, start_col) == 40

    def test_no_splitters(self):
        """Test with no splitters - only 1 timeline."""
        input_text = """S.
.."""
        grid, start_row, start_col = parse(input_text)
        assert part2(grid, start_row, start_col) == 1

    def test_single_splitter(self):
        """Test with a single splitter."""
        input_text = """S
^"""
        grid, start_row, start_col = parse(input_text)
        # Particle hits splitter, splits into 2 timelines (left and right)
        # Both exit the grid, so 2 unique timelines
        assert part2(grid, start_row, start_col) == 2

    def test_two_splitters_cascading(self):
        """Test with two splitters in cascade."""
        input_text = """...S...
...^...
..^.^..
"""
        grid, start_row, start_col = parse(input_text)
        # First split at row 1: 2 beams (left and right)
        # Both hit splitters at row 2: 2 * 2 = 4 timelines
        assert part2(grid, start_row, start_col) == 4

