"""Tests for Day 8 solution"""

import pytest
from .day08 import parse, part1, part2, euclidean_distance
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        boxes = parse(EXAMPLE_INPUT)
        assert len(boxes) == 20
        assert boxes[0] == (162, 817, 812)
        assert boxes[1] == (57, 618, 57)
        assert boxes[-1] == (425, 690, 689)

    def test_parse_single_box(self):
        """Test parsing a single junction box."""
        input_text = "1,2,3"
        boxes = parse(input_text)
        assert len(boxes) == 1
        assert boxes[0] == (1, 2, 3)

    def test_parse_multiple_boxes(self):
        """Test parsing multiple junction boxes."""
        input_text = """10,20,30
40,50,60
70,80,90"""
        boxes = parse(input_text)
        assert len(boxes) == 3
        assert boxes[0] == (10, 20, 30)
        assert boxes[1] == (40, 50, 60)
        assert boxes[2] == (70, 80, 90)


class TestDistance:
    def test_distance_same_point(self):
        """Test distance from a point to itself."""
        dist = euclidean_distance((0, 0, 0), (0, 0, 0))
        assert dist == 0.0

    def test_distance_simple(self):
        """Test simple distance calculation."""
        # Distance from origin to (3, 4, 0) should be 5
        dist = euclidean_distance((0, 0, 0), (3, 4, 0))
        assert abs(dist - 5.0) < 0.001

    def test_distance_3d(self):
        """Test 3D distance calculation."""
        # Distance from (1, 2, 3) to (4, 6, 8)
        # sqrt((4-1)^2 + (6-2)^2 + (8-3)^2) = sqrt(9 + 16 + 25) = sqrt(50)
        dist = euclidean_distance((1, 2, 3), (4, 6, 8))
        expected = 50 ** 0.5
        assert abs(dist - expected) < 0.001


class TestPart1:
    def test_example(self):
        """Test with the example from problem description."""
        boxes = parse(EXAMPLE_INPUT)
        # After 10 connections: 5*4*2 = 40
        result = part1(boxes, num_connections=10)
        assert result == 40

    def test_single_box(self):
        """Test with a single box - no connections possible."""
        boxes = [(0, 0, 0)]
        result = part1(boxes, num_connections=0)
        # One circuit of size 1: 1*1*1 = 1
        assert result == 1

    def test_two_boxes_no_connection(self):
        """Test with two boxes but no connection."""
        boxes = [(0, 0, 0), (10, 10, 10)]
        result = part1(boxes, num_connections=0)
        # Two circuits of size 1 each: 1*1*1 = 1
        assert result == 1

    def test_two_boxes_one_connection(self):
        """Test with two boxes and one connection."""
        boxes = [(0, 0, 0), (10, 10, 10)]
        result = part1(boxes, num_connections=1)
        # One circuit of size 2: 2*1*1 = 2
        assert result == 2

    def test_three_boxes_all_connected(self):
        """Test with three boxes all connected."""
        boxes = [(0, 0, 0), (1, 0, 0), (2, 0, 0)]
        result = part1(boxes, num_connections=2)
        # One circuit of size 3: 3*1*1 = 3
        assert result == 3


class TestPart2:
    def test_example(self):
        """Test with the example from problem description."""
        boxes = parse(EXAMPLE_INPUT)
        result = part2(boxes)
        # Last connection: 216,146,977 and 117,168,530
        # Product: 216 * 117 = 25272
        assert result == 25272

    def test_two_boxes(self):
        """Test with two boxes."""
        boxes = [(5, 0, 0), (10, 0, 0)]
        result = part2(boxes)
        # Only connection: 5 * 10 = 50
        assert result == 50

    def test_three_boxes_line(self):
        """Test with three boxes in a line."""
        boxes = [(1, 0, 0), (2, 0, 0), (10, 0, 0)]
        # Closest pairs:
        # (1,0,0)-(2,0,0): dist=1
        # (2,0,0)-(10,0,0): dist=8
        # (1,0,0)-(10,0,0): dist=9
        # Order: first connect (1,0,0)-(2,0,0), then (2,0,0)-(10,0,0)
        # Last connection: 2 * 10 = 20
        result = part2(boxes)
        assert result == 20

    def test_three_boxes_triangle(self):
        """Test with three boxes forming a triangle."""
        boxes = [(0, 0, 0), (3, 0, 0), (0, 4, 0)]
        # Distances:
        # (0,0,0)-(3,0,0): 3
        # (0,0,0)-(0,4,0): 4
        # (3,0,0)-(0,4,0): 5
        # Order: connect (0,0,0)-(3,0,0), then (0,0,0)-(0,4,0)
        # Last connection: 0 * 0 = 0
        result = part2(boxes)
        assert result == 0
