"""Tests for Day 6 solution"""

import pytest
from .day06 import parse_part1, evaluate_problem, solve_worksheet, part1, part2, PuzzleInput, Problem
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        input = parse_part1(EXAMPLE_INPUT)
        assert len(input.problems) == 4

        # Problem 1: 123 * 45 * 6
        assert input.problems[0].numbers == [123, 45, 6]
        assert input.problems[0].operation == '*'

        # Problem 2: 328 + 64 + 98
        assert input.problems[1].numbers == [328, 64, 98]
        assert input.problems[1].operation == '+'

        # Problem 3: 51 * 387 * 215
        assert input.problems[2].numbers == [51, 387, 215]
        assert input.problems[2].operation == '*'

        # Problem 4: 64 + 23 + 314
        assert input.problems[3].numbers == [64, 23, 314]
        assert input.problems[3].operation == '+'

    def test_parse_simple(self):
        """Test parsing a simple worksheet."""
        input_text = """10 20
5  3
+  *"""
        input = parse_part1(input_text)
        assert len(input.problems) == 2
        assert input.problems[0].numbers == [10, 5]
        assert input.problems[0].operation == '+'
        assert input.problems[1].numbers == [20, 3]
        assert input.problems[1].operation == '*'

    def test_parse_single_problem(self):
        """Test parsing a single problem."""
        input_text = """100
50
25
*"""
        input = parse_part1(input_text)
        assert len(input.problems) == 1
        assert input.problems[0].numbers == [100, 50, 25]
        assert input.problems[0].operation == '*'


class TestEvaluateProblem:
    def test_multiply_simple(self):
        """Test multiplication problem."""
        problem = Problem([123, 45, 6], '*')
        assert evaluate_problem(problem) == 33210

    def test_add_simple(self):
        """Test addition problem."""
        problem = Problem([328, 64, 98], '+')
        assert evaluate_problem(problem) == 490

    def test_multiply_two_numbers(self):
        """Test multiplication with two numbers."""
        problem = Problem([10, 5], '*')
        assert evaluate_problem(problem) == 50

    def test_add_two_numbers(self):
        """Test addition with two numbers."""
        problem = Problem([10, 5], '+')
        assert evaluate_problem(problem) == 15

    def test_single_number(self):
        """Test with single number."""
        problem = Problem([42], '+')
        assert evaluate_problem(problem) == 42


class TestSolveWorksheet:
    def test_example(self):
        """Test the example worksheet."""
        input = parse_part1(EXAMPLE_INPUT)
        assert solve_worksheet(input.problems) == 4277556

    def test_simple(self):
        """Test a simple worksheet."""
        problems = [
            Problem([10, 5], '+'),  # 15
            Problem([3, 4], '*'),   # 12
        ]
        assert solve_worksheet(problems) == 27


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        input = parse_part1(EXAMPLE_INPUT)
        assert part1(input) == 4277556

    def test_simple_case(self):
        """Test with a simple case."""
        input_text = """10 20
5  3
+  *"""
        input = parse_part1(input_text)
        # 10 + 5 = 15, 20 * 3 = 60, total = 75
        assert part1(input) == 75


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        input = parse_cephalopod_reading(EXAMPLE_INPUT)
        # 1058 + 3253600 + 625 + 8544 = 3263827
        assert part2(input) == 3263827

    def test_simple_case(self):
        """Test with a simple case."""
        input_text = """12 34
56 78
+  *"""
        input = parse_cephalopod_reading(input_text)
        # Problem 1: 48 * 37 = 1776
        # Problem 2: 26 + 15 = 41
        # Total: 1776 + 41 = 1817
        assert part2(input) == 1817
