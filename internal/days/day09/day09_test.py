"""Tests for Day 9 solution"""

import pytest
from .day09 import parse, part1, part2, calculate_rectangle_area
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        tiles = parse(EXAMPLE_INPUT)
        assert len(tiles) == 8
        assert (7, 1) in tiles
        assert (11, 1) in tiles
        assert (2, 3) in tiles

    def test_parse_single_tile(self):
        """Test parsing a single tile."""
        tiles = parse("5,10")
        assert len(tiles) == 1
        assert tiles[0] == (5, 10)

    def test_parse_multiple_tiles(self):
        """Test parsing multiple tiles."""
        input_text = """1,2
3,4
5,6"""
        tiles = parse(input_text)
        assert len(tiles) == 3
        assert tiles[0] == (1, 2)
        assert tiles[1] == (3, 4)
        assert tiles[2] == (5, 6)


class TestRectangleArea:
    def test_area_simple(self):
        """Test simple rectangle area calculation."""
        area = calculate_rectangle_area((0, 0), (3, 4))
        assert area == 20  # 4 * 5 (inclusive)

    def test_area_reversed_coords(self):
        """Test that order doesn't matter."""
        area1 = calculate_rectangle_area((0, 0), (3, 4))
        area2 = calculate_rectangle_area((3, 4), (0, 0))
        assert area1 == area2

    def test_area_negative_coords(self):
        """Test with negative coordinates."""
        area = calculate_rectangle_area((-2, -3), (2, 3))
        assert area == 35  # 5 * 7 (inclusive)

    def test_area_same_point(self):
        """Test when both corners are the same point."""
        area = calculate_rectangle_area((5, 5), (5, 5))
        assert area == 1  # Single tile

    def test_area_example_24(self):
        """Test example with area 24."""
        area = calculate_rectangle_area((2, 5), (9, 7))
        assert area == 24  # 8 * 3

    def test_area_example_35(self):
        """Test example with area 35."""
        area = calculate_rectangle_area((7, 1), (11, 7))
        assert area == 35  # 5 * 7

    def test_area_example_50(self):
        """Test example with area 50."""
        area = calculate_rectangle_area((2, 5), (11, 1))
        assert area == 50  # 10 * 5


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        tiles = parse(EXAMPLE_INPUT)
        result = part1(tiles)
        assert result == 50

    def test_two_tiles(self):
        """Test with two tiles."""
        tiles = [(0, 0), (5, 10)]
        result = part1(tiles)
        assert result == 66  # 6 * 11 (inclusive)

    def test_three_tiles_max(self):
        """Test with three tiles - should find max."""
        tiles = [(0, 0), (1, 1), (10, 10)]
        # Pairs: (0,0)-(1,1)=4, (0,0)-(10,10)=121, (1,1)-(10,10)=100
        result = part1(tiles)
        assert result == 121

    def test_single_tile(self):
        """Test with single tile - area should be 0."""
        tiles = [(5, 5)]
        result = part1(tiles)
        assert result == 0


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        tiles = parse(EXAMPLE_INPUT)
        result = part2(tiles)
        assert result == 24

    def test_small_square(self):
        """Test with a small square loop."""
        # Square loop: (0,0) -> (2,0) -> (2,2) -> (0,2) -> back to (0,0)
        tiles = [(0, 0), (2, 0), (2, 2), (0, 2)]
        result = part2(tiles)
        # All tiles in the 3x3 grid are valid
        # Largest rectangle is the whole thing: 3x3 = 9
        assert result == 9

    def test_rectangle_outside_polygon(self):
        """Test that rectangles outside polygon are rejected."""
        # Simple square
        tiles = [(0, 0), (5, 0), (5, 5), (0, 5)]
        # Try to make rectangle from (0,0) to (10, 10) - should fail
        # Maximum should be within the 6x6 square = 36
        result = part2(tiles)
        assert result == 36
