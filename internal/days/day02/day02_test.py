"""Tests for Day 2 solution"""

import pytest
from .day02 import is_invalid_id, is_invalid_id_part2, parse, part1, part2
from .input import EXAMPLE_INPUT


class TestIsInvalidId:
    def test_single_digit_repeated(self):
        """Test single digit repeated twice."""
        assert is_invalid_id(11) == True
        assert is_invalid_id(22) == True
        assert is_invalid_id(55) == True
        assert is_invalid_id(99) == True

    def test_two_digit_repeated(self):
        """Test two-digit sequence repeated."""
        assert is_invalid_id(6464) == True
        assert is_invalid_id(1010) == True
        assert is_invalid_id(9999) == True

    def test_three_digit_repeated(self):
        """Test three-digit sequence repeated."""
        assert is_invalid_id(123123) == True
        assert is_invalid_id(999999) == True

    def test_large_repeated_sequence(self):
        """Test large sequences from the example."""
        assert is_invalid_id(1188511885) == True  # 11885 repeated
        assert is_invalid_id(222222) == True  # 222 repeated
        assert is_invalid_id(446446) == True  # 446 repeated
        assert is_invalid_id(38593859) == True  # 3859 repeated

    def test_valid_ids(self):
        """Test IDs that are NOT invalid (should return False)."""
        assert is_invalid_id(12) == False
        assert is_invalid_id(101) == False  # Not 0101
        assert is_invalid_id(123) == False
        assert is_invalid_id(1234) == False
        assert is_invalid_id(12345) == False

    def test_odd_length_numbers(self):
        """Test odd-length numbers cannot be invalid."""
        assert is_invalid_id(1) == False
        assert is_invalid_id(111) == False
        assert is_invalid_id(12312) == False

    def test_no_leading_zeros(self):
        """Test that numbers with implied leading zeros are not invalid."""
        # 0101 isn't a valid ID at all (101 is the ID, not 0101)
        assert is_invalid_id(101) == False


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        ranges = parse(EXAMPLE_INPUT)
        expected = [
            (11, 22),
            (95, 115),
            (998, 1012),
            (1188511880, 1188511890),
            (222220, 222224),
            (1698522, 1698528),
            (446443, 446449),
            (38593856, 38593862),
            (565653, 565659),
            (824824821, 824824827),
            (2121212118, 2121212124),
        ]
        assert ranges == expected

    def test_parse_single_range(self):
        """Test parsing a single range."""
        ranges = parse("10-20")
        assert ranges == [(10, 20)]

    def test_parse_multiple_ranges(self):
        """Test parsing multiple ranges."""
        ranges = parse("1-10,20-30,40-50")
        assert ranges == [(1, 10), (20, 30), (40, 50)]


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        ranges = parse(EXAMPLE_INPUT)
        assert part1(ranges) == 1227775554

    def test_range_11_22(self):
        """Test range 11-22 has invalid IDs 11 and 22."""
        ranges = [(11, 22)]
        # Invalid IDs: 11, 22
        expected = 11 + 22
        assert part1(ranges) == expected

    def test_range_95_115(self):
        """Test range 95-115 has invalid ID 99."""
        ranges = [(95, 115)]
        # Invalid ID: 99
        assert part1(ranges) == 99

    def test_range_998_1012(self):
        """Test range 998-1012 has invalid ID 1010."""
        ranges = [(998, 1012)]
        # Invalid ID: 1010
        assert part1(ranges) == 1010

    def test_range_no_invalid_ids(self):
        """Test range with no invalid IDs."""
        ranges = [(1698522, 1698528)]
        # No invalid IDs in this range
        assert part1(ranges) == 0

    def test_empty_range_list(self):
        """Test empty range list."""
        ranges = []
        assert part1(ranges) == 0


class TestIsInvalidIdPart2:
    def test_repeated_twice(self):
        """Test patterns repeated exactly twice (should still be invalid)."""
        assert is_invalid_id_part2(11) == True
        assert is_invalid_id_part2(22) == True
        assert is_invalid_id_part2(6464) == True
        assert is_invalid_id_part2(1010) == True
        assert is_invalid_id_part2(123123) == True
        assert is_invalid_id_part2(12341234) == True

    def test_repeated_three_times(self):
        """Test patterns repeated three times."""
        assert is_invalid_id_part2(111) == True
        assert is_invalid_id_part2(999) == True
        assert is_invalid_id_part2(123123123) == True

    def test_repeated_five_times(self):
        """Test patterns repeated five times."""
        assert is_invalid_id_part2(1212121212) == True

    def test_repeated_seven_times(self):
        """Test patterns repeated seven times."""
        assert is_invalid_id_part2(1111111) == True

    def test_large_repeated_sequences(self):
        """Test large sequences from the example."""
        assert is_invalid_id_part2(1188511885) == True  # 11885 repeated twice
        assert is_invalid_id_part2(222222) == True  # 222 repeated twice OR 22 repeated 3 times OR 2 repeated 6 times
        assert is_invalid_id_part2(446446) == True  # 446 repeated twice
        assert is_invalid_id_part2(38593859) == True  # 3859 repeated twice
        assert is_invalid_id_part2(565656) == True  # 56 repeated 3 times
        assert is_invalid_id_part2(824824824) == True  # 824 repeated 3 times
        assert is_invalid_id_part2(2121212121) == True  # 21 repeated 5 times

    def test_valid_ids(self):
        """Test IDs that are NOT invalid (should return False)."""
        assert is_invalid_id_part2(12) == False
        assert is_invalid_id_part2(101) == False
        assert is_invalid_id_part2(123) == False
        assert is_invalid_id_part2(1234) == False
        assert is_invalid_id_part2(12345) == False
        assert is_invalid_id_part2(1698522) == False

    def test_single_digit(self):
        """Test single digits are not invalid (can't repeat at least twice)."""
        assert is_invalid_id_part2(1) == False
        assert is_invalid_id_part2(9) == False


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        ranges = parse(EXAMPLE_INPUT)
        assert part2(ranges) == 4174379265

    def test_range_11_22(self):
        """Test range 11-22 has invalid IDs 11 and 22."""
        ranges = [(11, 22)]
        # Invalid IDs: 11, 22
        expected = 11 + 22
        assert part2(ranges) == expected

    def test_range_95_115(self):
        """Test range 95-115 has invalid IDs 99 and 111."""
        ranges = [(95, 115)]
        # Invalid IDs: 99, 111
        expected = 99 + 111
        assert part2(ranges) == expected

    def test_range_998_1012(self):
        """Test range 998-1012 has invalid IDs 999 and 1010."""
        ranges = [(998, 1012)]
        # Invalid IDs: 999, 1010
        expected = 999 + 1010
        assert part2(ranges) == expected

    def test_range_565653_565659(self):
        """Test range 565653-565659 has invalid ID 565656."""
        ranges = [(565653, 565659)]
        # Invalid ID: 565656 (56 repeated 3 times)
        expected = 565656
        assert part2(ranges) == expected

    def test_range_824824821_824824827(self):
        """Test range 824824821-824824827 has invalid ID 824824824."""
        ranges = [(824824821, 824824827)]
        # Invalid ID: 824824824 (824 repeated 3 times)
        expected = 824824824
        assert part2(ranges) == expected

    def test_range_2121212118_2121212124(self):
        """Test range 2121212118-2121212124 has invalid ID 2121212121."""
        ranges = [(2121212118, 2121212124)]
        # Invalid ID: 2121212121 (21 repeated 5 times)
        expected = 2121212121
        assert part2(ranges) == expected

    def test_range_no_invalid_ids(self):
        """Test range with no invalid IDs."""
        ranges = [(1698522, 1698528)]
        # No invalid IDs in this range
        assert part2(ranges) == 0

    def test_empty_range_list(self):
        """Test empty range list."""
        ranges = []
        assert part2(ranges) == 0
