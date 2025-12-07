"""Tests for Day 7 solution"""

import pytest
from .day07 import parse, part1
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

    def test_find_start(self):
        """Test finding the start position."""
        input_text = """...
.S.
..."""
        grid, start_row, start_col = parse(input_text)
        assert start_row == 1
        assert start_col == 1


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

    def test_single_splitter(self):
        """Test with a single splitter."""
        input_text = """S.
.^"""
        grid, start_row, start_col = parse(input_text)
        # Beam moves down from S at (0,0) to (1,0), then exits
        # Splitter is at (1,1), so beam never hits it
        assert part1(grid, start_row, start_col) == 0

    def test_beam_exits_bounds(self):
        """Test when beam exits bounds."""
        input_text = """S.
.."""
        grid, start_row, start_col = parse(input_text)
        assert part1(grid, start_row, start_col) == 0

    def test_multiple_splitters_in_line(self):
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

