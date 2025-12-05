"""Tests for Day 4 solution"""

import pytest
from .day04 import parse, part1, part2, count_accessible_rolls, count_removable_rolls, is_accessible
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        grid = parse(EXAMPLE_INPUT)
        assert len(grid) == 10
        assert len(grid[0]) == 10
        assert grid[0] == [0, 0, 1, 1, 0, 1, 1, 1, 1, 0]
        assert grid[1] == [1, 1, 1, 0, 1, 0, 1, 0, 1, 1]

    def test_parse_single_line(self):
        """Test parsing a single line."""
        grid = parse("@.@")
        assert grid == [[1, 0, 1]]

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        grid = parse("")
        assert grid == []


class TestIsAccessible:
    def test_corner_with_no_neighbors(self):
        """Test corner position with no @ neighbors."""
        grid = parse("@...\n....\n....")
        assert is_accessible(grid, 0, 0) == True

    def test_corner_with_three_neighbors(self):
        """Test corner position with 3 @ neighbors."""
        grid = parse("@@..\n@@..")
        assert is_accessible(grid, 0, 0) == True

    def test_corner_with_four_neighbors(self):
        """Test corner position with 4 neighbors (not accessible)."""
        # Top-left has only 3 possible neighbors, so can't have 4
        # Use a different example
        grid = parse(".....\n.@@@.\n.@@@.\n.@@@.")
        # Center @ at (2,2) has 8 neighbors, all @
        assert is_accessible(grid, 2, 2) == False

    def test_center_with_few_neighbors(self):
        """Test center position with < 4 @ neighbors."""
        grid = parse(".....\n..@..\n.@@@.\n..@..\n.....")
        # Center @ at (2,2) has 4 @ neighbors (N,S,E,W)
        assert is_accessible(grid, 2, 2) == False
        # @ at (1,2) has 1 @ neighbor
        assert is_accessible(grid, 1, 2) == True

    def test_edge_position(self):
        """Test edge position."""
        grid = parse("@@@@@\n@@@@@")
        # Top edge @ at (0,2) has 5 neighbors
        assert is_accessible(grid, 0, 2) == False


class TestCountAccessibleRolls:
    def test_example(self):
        """Test the full example."""
        grid = parse(EXAMPLE_INPUT)
        assert count_accessible_rolls(grid) == 13

    def test_single_roll(self):
        """Test grid with single roll."""
        grid = parse("@")
        assert count_accessible_rolls(grid) == 1

    def test_two_rolls_adjacent(self):
        """Test two adjacent rolls."""
        grid = parse("@@")
        assert count_accessible_rolls(grid) == 2

    def test_grid_with_all_accessible(self):
        """Test grid where all rolls are accessible."""
        grid = parse("@.@.@\n.....\n@.@.@")
        assert count_accessible_rolls(grid) == 6

    def test_grid_with_few_accessible(self):
        """Test grid where no rolls are accessible."""
        grid = parse("@@@@@\n@@@@@\n@@@@@")
        # All interior and edge @ have >= 4 neighbors
        # Corners have 3 neighbors, edges have 5, center has 8
        # So corners (4 of them) are accessible
        assert count_accessible_rolls(grid) == 4

    def test_empty_grid(self):
        """Test empty grid."""
        grid = []
        assert count_accessible_rolls(grid) == 0

    def test_no_rolls(self):
        """Test grid with no rolls."""
        grid = parse("....\n....")
        assert count_accessible_rolls(grid) == 0


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        grid = parse(EXAMPLE_INPUT)
        assert part1(grid) == 13

    def test_simple_grid(self):
        """Test with a simple grid."""
        grid = parse("@.@")
        assert part1(grid) == 2


class TestCountRemovableRolls:
    def test_example(self):
        """Test the full example for Part 2."""
        grid = parse(EXAMPLE_INPUT)
        assert count_removable_rolls(grid) == 43

    def test_single_roll(self):
        """Test grid with single roll."""
        grid = parse("@")
        assert count_removable_rolls(grid) == 1

    def test_two_isolated_rolls(self):
        """Test two isolated rolls."""
        grid = parse("@.@")
        # Both are accessible and can be removed
        assert count_removable_rolls(grid) == 2

    def test_cluster_that_breaks_down(self):
        """Test cluster where removal creates new accessible rolls."""
        grid = parse("@@@\n@@@\n@@@")
        # 3x3 grid: corners have 3 neighbors (accessible)
        # After removing corners, edges become accessible, etc.
        # Corners: 4 rolls
        # After first pass, should expose more
        assert count_removable_rolls(grid) == 9

    def test_no_rolls(self):
        """Test grid with no rolls."""
        grid = parse("....\n....")
        assert count_removable_rolls(grid) == 0

    def test_empty_grid(self):
        """Test empty grid."""
        grid = []
        assert count_removable_rolls(grid) == 0


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        grid = parse(EXAMPLE_INPUT)
        assert part2(grid) == 43

    def test_simple_grid(self):
        """Test with a simple grid."""
        grid = parse("@.@")
        assert part2(grid) == 2
