"""Tests for Day 12: Present Packing"""

import pytest
from .day12 import (
    parse_shapes, parse_regions, normalize_shape, generate_transformations,
    can_fit_presents, parse, part1
)
from .input import EXAMPLE_INPUT


class TestParseShapes:
    """Test parsing of present shapes."""

    def test_parse_single_shape(self):
        """Test parsing a single shape."""
        input_text = """0:
###
##.
##."""
        shapes = parse_shapes(input_text)

        assert len(shapes) == 1
        assert 0 in shapes
        # Shape 0 has # at positions (0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (2,1)
        expected = {(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (2,1)}
        assert shapes[0] == expected

    def test_parse_shape_with_dots(self):
        """Test parsing shape 4 which has dots in the middle."""
        input_text = """4:
###
#..
###"""
        shapes = parse_shapes(input_text)

        assert len(shapes) == 1
        # Shape 4: row 0 all #, row 1 only first #, row 2 all #
        expected = {(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)}
        assert shapes[4] == expected

    def test_parse_shape_5(self):
        """Test parsing shape 5 (cross pattern)."""
        input_text = """5:
###
.#.
###"""
        shapes = parse_shapes(input_text)

        # Shape 5: cross pattern
        expected = {(0,0), (0,1), (0,2), (1,1), (2,0), (2,1), (2,2)}
        assert shapes[5] == expected

    def test_parse_all_example_shapes(self):
        """Test parsing all shapes from example."""
        shapes = parse_shapes(EXAMPLE_INPUT)

        assert len(shapes) == 6
        assert all(i in shapes for i in range(6))


class TestNormalizeShape:
    """Test shape normalization."""

    def test_normalize_already_normalized(self):
        """Test normalizing a shape that's already at (0,0)."""
        shape = {(0,0), (0,1), (1,0)}
        normalized = normalize_shape(shape)
        assert normalized == shape

    def test_normalize_offset_shape(self):
        """Test normalizing a shape with offset."""
        shape = {(2,3), (2,4), (3,3)}
        normalized = normalize_shape(shape)
        assert normalized == {(0,0), (0,1), (1,0)}

    def test_normalize_negative_coords(self):
        """Test normalizing with negative coordinates."""
        shape = {(-1,-2), (-1,-1), (0,-2)}
        normalized = normalize_shape(shape)
        assert normalized == {(0,0), (0,1), (1,0)}


class TestGenerateTransformations:
    """Test generating rotations and flips of shapes."""

    def test_single_cell(self):
        """Test transformations of a single cell."""
        shape = {(0,0)}
        transformations = generate_transformations(shape)
        # All transformations should be the same for a single cell
        assert len(transformations) == 1
        assert transformations[0] == {(0,0)}

    def test_line_shape(self):
        """Test transformations of a 3-cell line."""
        shape = {(0,0), (0,1), (0,2)}  # Horizontal line
        transformations = generate_transformations(shape)

        # Should have horizontal and vertical orientations
        assert len(transformations) >= 2
        # Check that vertical line is one of the transformations
        vertical = {(0,0), (1,0), (2,0)}
        assert any(t == vertical for t in transformations)

    def test_asymmetric_shape(self):
        """Test transformations of an asymmetric shape."""
        # L-shape
        shape = {(0,0), (1,0), (2,0), (2,1)}
        transformations = generate_transformations(shape)

        # Should have multiple unique transformations
        assert len(transformations) >= 4
        # All transformations should have same number of cells
        assert all(len(t) == 4 for t in transformations)


class TestParseRegions:
    """Test parsing of regions and required presents."""

    def test_parse_single_region(self):
        """Test parsing a single region."""
        input_text = "4x4: 0 0 0 0 2 0"
        regions = parse_regions(input_text)

        assert len(regions) == 1
        width, height, required = regions[0]
        assert width == 4
        assert height == 4
        assert required == [0, 0, 0, 0, 2, 0]

    def test_parse_region_12x5(self):
        """Test parsing a 12x5 region."""
        input_text = "12x5: 1 0 1 0 2 2"
        regions = parse_regions(input_text)

        assert len(regions) == 1
        width, height, required = regions[0]
        assert width == 12
        assert height == 5
        assert required == [1, 0, 1, 0, 2, 2]

    def test_parse_all_example_regions(self):
        """Test parsing all regions from example."""
        regions = parse_regions(EXAMPLE_INPUT)

        assert len(regions) == 3
        # First region: 4x4 with presents [0,0,0,0,2,0]
        assert regions[0] == (4, 4, [0, 0, 0, 0, 2, 0])
        # Second region: 12x5 with presents [1,0,1,0,2,2]
        assert regions[1] == (12, 5, [1, 0, 1, 0, 2, 2])
        # Third region: 12x5 with presents [1,0,1,0,3,2]
        assert regions[2] == (12, 5, [1, 0, 1, 0, 3, 2])


class TestCanFitPresents:
    """Test the present fitting algorithm."""

    def test_single_present_fits(self):
        """Test that a single present can fit in a region."""
        # Shape: single cell
        shapes = {0: {(0,0)}}
        # Region: 2x2, need 1 of shape 0
        width, height, required = 2, 2, [1]

        assert can_fit_presents(width, height, shapes, required) is True

    def test_present_too_large(self):
        """Test that a present that's too large doesn't fit."""
        # Shape: 3x1 line
        shapes = {0: {(0,0), (0,1), (0,2)}}
        # Region: 2x2, need 1 of shape 0
        width, height, required = 2, 2, [1]

        # Even with rotation, can't fit 3-cell line in 2x2
        assert can_fit_presents(width, height, shapes, required) is False

    def test_example_4x4_region(self):
        """Test the first example region (4x4 with two shape-4 presents)."""
        # Shape 4: ###, #.., ###
        shape4 = {(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)}
        shapes = {4: shape4}

        # Region: 4x4, need 2 of shape 4
        width, height, required = 4, 4, [0, 0, 0, 0, 2, 0]

        assert can_fit_presents(width, height, shapes, required) is True

    def test_example_12x5_success(self):
        """Test the second example region (should fit)."""
        # Parse all shapes from example
        shapes = parse_shapes(EXAMPLE_INPUT)

        # Region: 12x5 with [1,0,1,0,2,2]
        width, height, required = 12, 5, [1, 0, 1, 0, 2, 2]

        assert can_fit_presents(width, height, shapes, required) is True

    def test_example_12x5_failure(self):
        """Test the third example region (should not fit)."""
        # Parse all shapes from example
        shapes = parse_shapes(EXAMPLE_INPUT)

        # Region: 12x5 with [1,0,1,0,3,2] (one more shape-4 than previous)
        width, height, required = 12, 5, [1, 0, 1, 0, 3, 2]

        assert can_fit_presents(width, height, shapes, required) is False


class TestPart1:
    """Test part 1 solution."""

    def test_example(self):
        """Test with the example from problem description."""
        data = parse(EXAMPLE_INPUT)
        result = part1(data)

        # 2 out of 3 regions can fit all presents
        assert result == 2
