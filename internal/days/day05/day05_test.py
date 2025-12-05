"""Tests for Day 5 solution"""

import pytest
from .day05 import parse, is_fresh, count_fresh_ingredients, part1
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        input = parse(EXAMPLE_INPUT)
        assert input.ranges == [(3, 5), (10, 14), (16, 20), (12, 18)]
        assert input.ingredient_ids == [1, 5, 8, 11, 17, 32]

    def test_parse_single_range(self):
        """Test parsing a single range."""
        input = parse("1-3\n\n5")
        assert input.ranges == [(1, 3)]
        assert input.ingredient_ids == [5]

    def test_parse_empty_ranges(self):
        """Test parsing with no ranges."""
        input = parse("\n\n5\n10")
        assert input.ranges == []
        assert input.ingredient_ids == [5, 10]


class TestIsFresh:
    def test_id_in_single_range(self):
        """Test ID that falls in a single range."""
        ranges = [(3, 5)]
        assert is_fresh(4, ranges) == True
        assert is_fresh(3, ranges) == True
        assert is_fresh(5, ranges) == True

    def test_id_outside_range(self):
        """Test ID that doesn't fall in any range."""
        ranges = [(3, 5), (10, 14)]
        assert is_fresh(1, ranges) == False
        assert is_fresh(8, ranges) == False
        assert is_fresh(32, ranges) == False

    def test_id_in_overlapping_ranges(self):
        """Test ID that falls in overlapping ranges."""
        ranges = [(10, 14), (12, 18)]
        assert is_fresh(13, ranges) == True

    def test_id_at_range_boundaries(self):
        """Test IDs at range boundaries."""
        ranges = [(10, 14)]
        assert is_fresh(10, ranges) == True
        assert is_fresh(14, ranges) == True
        assert is_fresh(9, ranges) == False
        assert is_fresh(15, ranges) == False

    def test_no_ranges(self):
        """Test with no ranges (all spoiled)."""
        ranges = []
        assert is_fresh(5, ranges) == False


class TestCountFreshIngredients:
    def test_example(self):
        """Test the full example."""
        input = parse(EXAMPLE_INPUT)
        assert count_fresh_ingredients(input.ranges, input.ingredient_ids) == 3

    def test_all_fresh(self):
        """Test when all ingredients are fresh."""
        ranges = [(1, 100)]
        ingredient_ids = [5, 10, 50, 100]
        assert count_fresh_ingredients(ranges, ingredient_ids) == 4

    def test_all_spoiled(self):
        """Test when all ingredients are spoiled."""
        ranges = [(1, 5)]
        ingredient_ids = [10, 20, 30]
        assert count_fresh_ingredients(ranges, ingredient_ids) == 0

    def test_mixed(self):
        """Test mixed fresh and spoiled."""
        ranges = [(1, 5), (10, 15)]
        ingredient_ids = [3, 7, 12, 20]
        # Fresh: 3, 12 (2 total)
        assert count_fresh_ingredients(ranges, ingredient_ids) == 2

    def test_empty_ingredients(self):
        """Test with no ingredients."""
        ranges = [(1, 5)]
        ingredient_ids = []
        assert count_fresh_ingredients(ranges, ingredient_ids) == 0


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        input = parse(EXAMPLE_INPUT)
        assert part1(input) == 3

    def test_simple_case(self):
        """Test with a simple case."""
        input_text = "1-5\n\n3\n7"
        input = parse(input_text)
        assert part1(input) == 1
