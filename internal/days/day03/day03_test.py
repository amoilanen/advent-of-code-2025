"""Tests for Day 3 solution"""

import pytest
from .day03 import max_joltage, max_joltage_n, parse, part1, part2
from .input import EXAMPLE_INPUT


class TestMaxJoltage:
    def test_example_bank1(self):
        """Test bank 987654321111111 produces 98."""
        assert max_joltage("987654321111111") == 98

    def test_example_bank2(self):
        """Test bank 811111111111119 produces 89."""
        assert max_joltage("811111111111119") == 89

    def test_example_bank3(self):
        """Test bank 234234234234278 produces 78."""
        assert max_joltage("234234234234278") == 78

    def test_example_bank4(self):
        """Test bank 818181911112111 produces 92."""
        assert max_joltage("818181911112111") == 92

    def test_simple_ascending(self):
        """Test simple ascending sequence."""
        assert max_joltage("123") == 23

    def test_simple_descending(self):
        """Test simple descending sequence."""
        assert max_joltage("321") == 32

    def test_two_digits(self):
        """Test with exactly two digits."""
        assert max_joltage("12") == 12
        assert max_joltage("99") == 99
        assert max_joltage("89") == 89

    def test_with_nines(self):
        """Test when 9 is available."""
        assert max_joltage("192") == 92
        assert max_joltage("219") == 29
        assert max_joltage("991") == 99

    def test_all_same_digits(self):
        """Test when all digits are the same."""
        assert max_joltage("1111") == 11
        assert max_joltage("5555") == 55


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        banks = parse(EXAMPLE_INPUT)
        expected = [
            "987654321111111",
            "811111111111119",
            "234234234234278",
            "818181911112111",
        ]
        assert banks == expected

    def test_parse_single_line(self):
        """Test parsing a single bank."""
        banks = parse("123")
        assert banks == ["123"]

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        banks = parse("")
        assert banks == []

    def test_parse_with_blank_lines(self):
        """Test parsing with blank lines."""
        banks = parse("123\n\n456")
        assert banks == ["123", "456"]


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        banks = parse(EXAMPLE_INPUT)
        assert part1(banks) == 357

    def test_single_bank(self):
        """Test with a single bank."""
        banks = ["987654321111111"]
        assert part1(banks) == 98

    def test_multiple_simple_banks(self):
        """Test with multiple simple banks."""
        banks = ["123", "456", "789"]
        # 23 + 56 + 89
        assert part1(banks) == 168

    def test_empty_banks(self):
        """Test with empty list."""
        banks = []
        assert part1(banks) == 0


class TestMaxJoltageN:
    def test_example_bank1_part2(self):
        """Test bank 987654321111111 with 12 batteries produces 987654321111."""
        assert max_joltage_n("987654321111111", 12) == 987654321111

    def test_example_bank2_part2(self):
        """Test bank 811111111111119 with 12 batteries produces 811111111119."""
        assert max_joltage_n("811111111111119", 12) == 811111111119

    def test_example_bank3_part2(self):
        """Test bank 234234234234278 with 12 batteries produces 434234234278."""
        assert max_joltage_n("234234234234278", 12) == 434234234278

    def test_example_bank4_part2(self):
        """Test bank 818181911112111 with 12 batteries produces 888911112111."""
        assert max_joltage_n("818181911112111", 12) == 888911112111

    def test_select_all(self):
        """Test when n equals bank length."""
        assert max_joltage_n("123456", 6) == 123456
        assert max_joltage_n("987654", 6) == 987654

    def test_select_two(self):
        """Test selecting 2 batteries (should match max_joltage)."""
        assert max_joltage_n("987654321111111", 2) == 98
        assert max_joltage_n("123", 2) == 23

    def test_simple_cases(self):
        """Test simple selection cases."""
        # Select 3 from "12345" -> "345"
        assert max_joltage_n("12345", 3) == 345
        # Select 3 from "54321" -> "543"
        assert max_joltage_n("54321", 3) == 543

    def test_greedy_selection(self):
        """Test that greedy selection works correctly."""
        # "19234" select 3 -> should pick "9", "3", "4" = 934
        assert max_joltage_n("19234", 3) == 934
        # "12934" select 3 -> should pick "9", "3", "4" = 934
        assert max_joltage_n("12934", 3) == 934


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        banks = parse(EXAMPLE_INPUT)
        assert part2(banks) == 3121910778619

    def test_single_bank(self):
        """Test with a single bank."""
        banks = ["987654321111111"]
        assert part2(banks) == 987654321111

    def test_empty_banks(self):
        """Test with empty list."""
        banks = []
        assert part2(banks) == 0
